import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'

export const useKanbanStore = defineStore('kanban', () => {
  const kanban = ref([])

  const states = ref([])
  const setStates = (statesData) => {
    states.value = statesData
  }

  const tasks = ref([])
  const setTasks = (tasksData) => {
    tasks.value = tasksData
  }

  const members = ref([])
  const setMembers = (membersData) => {
    members.value = membersData
  }

  const priorities = ref([])
  const setPriorities = (prioritiesData) => {
    priorities.value = prioritiesData
  }

  const assigneeFilters = ref([])
  const taskTypes = ref([])
  const priorityFilters = ref([])

  const setupKanban = async () => {
    kanban.value = states.value.map((state) => {
      const stateTasks = tasks.value.filter((task) => {
        return task.stateId === state.id
      })

      return {
        tasks: stateTasks,
        ...state,
      }
    })
  }

  const addNewTask = (newTask) => {
    tasks.value.push(newTask)

    const state = kanban.value.find((state) => state.id === newTask.stateId)
    if (!state) return

    state.tasks.push(newTask)
  }

  const updateTask = (stateId, taskId, updatedTaskData) => {
    if (updatedTaskData.stateId !== stateId) {
      // stateId is changed

      const oldState = kanban.value.find((state) => state.id === stateId)
      const newState = kanban.value.find(
        (state) => state.id === updatedTaskData.stateId
      )

      oldState.tasks = oldState.tasks.filter(
        (task) => task.id !== updatedTaskData.id
      )
      newState.tasks.push(updatedTaskData)

      // Sort tasks in the new state by sequence
      newState.tasks.sort((a, b) => a.sequence - b.sequence)
    } else {
      // No stateId is changed
      const state = kanban.value.find((state) => state.id === stateId)
      if (!state) return false

      const taskIndex = state.tasks.findIndex((task) => task.id === taskId)
      if (taskIndex === -1) return false

      // Update the task in the state
      state.tasks[taskIndex] = { ...state.tasks[taskIndex], ...updatedTaskData }
    }

    // Also update the task in the tasks array
    const globalTaskIndex = tasks.value.findIndex((task) => task.id === taskId)
    if (globalTaskIndex !== -1) {
      tasks.value[globalTaskIndex] = {
        ...tasks.value[globalTaskIndex],
        ...updatedTaskData,
      }
    }
  }

  return {
    states,
    setStates,
    tasks,
    setTasks,
    setupKanban,
    kanban,
    members,
    setMembers,
    priorities,
    setPriorities,
    assigneeFilters,
    taskTypes,
    priorityFilters,
    addNewTask,
    updateTask,
  }
})
