import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useBoardStore = defineStore('board', () => {
    const states = ref([])
    const setStates = (statesData) => {
        states.value - statesData
    }

    const tasks = ref([])
    const setTasks = (tasksData) => {
        tasks.value = tasksData
    }

  return { states, setStates, tasks, setTasks }
})
