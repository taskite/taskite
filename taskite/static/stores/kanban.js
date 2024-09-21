import { ref, computed } from 'vue'
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

  const setupKanban = async () => {
    kanban.value = states.value.map((state) => {
      const stateTasks = tasks.value.filter((task) => task.stateId === state.id)

      return {
        tasks: stateTasks,
        ...state,
      }
    })
  }

  return { states, setStates, tasks, setTasks, setupKanban, kanban }
})
