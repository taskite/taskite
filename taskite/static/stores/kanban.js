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
    console.log(newTask)
    tasks.value.push(newTask)

    const state = kanban.value.find((state) => state.id === newTask.stateId)
    if (!state) return

    state.tasks.push(newTask)
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
  }
})
