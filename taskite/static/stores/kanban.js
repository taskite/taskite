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

  const labels = ref([])
  const setLabels = (labelsData) => {
    labels.value = labelsData
  }

  const assigneeFilters = ref([])
  const taskTypes = ref([])
  const priorityFilters = ref([])
  const labelFilters = ref([])

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

  const globalTaskUpdate = (updatedTaskData) => {
    const globalTaskIndex = tasks.value.findIndex(
      (task) => task.id === updatedTaskData.id
    )
    if (globalTaskIndex !== -1) {
      tasks.value[globalTaskIndex] = {
        ...tasks.value[globalTaskIndex],
        ...updatedTaskData,
      }
    }
  }

  const updateTaskState = (oldStateId, updatedTaskData) => {
    const oldState = kanban.value.find((state) => state.id === oldStateId)
    if (!oldState) return false

    const newState = kanban.value.find(
      (state) => state.id === updatedTaskData.stateId
    )
    if (!newState) return false

    // Remove task from old state
    oldState.tasks = oldState.tasks.filter(
      (task) => task.id !== updatedTaskData.id
    )

    // Push the data to new state
    newState.tasks.push(updatedTaskData)
    newState.tasks.sort((a, b) => a.sequence - b.sequence)

    // Also update the task in the tasks array
    globalTaskUpdate(updatedTaskData)
  }

  const updateTask = (updatedTaskData) => {
    const state = kanban.value.find(
      (state) => state.id === updatedTaskData.stateId
    )
    if (!state) return false

    const taskIndex = state.tasks.findIndex(
      (task) => task.id === updatedTaskData.id
    )
    if (taskIndex === -1) return false

    // Update the task in the state
    state.tasks[taskIndex] = { ...state.tasks[taskIndex], ...updatedTaskData }

    // Also update the task in the tasks array
    globalTaskUpdate(updatedTaskData)
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
    labels,
    setLabels,
    assigneeFilters,
    taskTypes,
    priorityFilters,
    labelFilters,
    addNewTask,
    updateTask,
    updateTaskState,
  }
})
