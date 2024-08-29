import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'

export const useBoardStore = defineStore('board', () => {
  const kanban = ref([])

  const setKanban = (kanbanData) => {
    kanban.value = kanbanData
  }

  const tasksCount = computed(() => {
    return kanban.value.map((state) => state.tasks).flat().length
  })

  const states = ref([])
  const setStates = (statesData) => {
    states.value = statesData
  }

  const members = ref([])
  const setMembers = (membersData) => {
    members.value = membersData
  }

  const priorities = ref([])
  const setPriorities = (prioritiesData) => {
    priorities.value = prioritiesData
  }

  const tasks = ref([])
  const setTasks = (tasksData) => {
    tasks.value = tasksData
  }

  const prioritiesFilter = ref([])

  const loadKanban = async () => {
    const kanbanData = states.value.map((state) => {
      var stateTasks = tasks.value.filter((task) => {
        // Check for priorities Filter
        if(prioritiesFilter.value.length > 0 && !prioritiesFilter.value.includes(task.priorityId)) return false

        return task.stateId === state.id
      })

      stateTasks = stateTasks.map(task => {
        return {
          ...task,
          priority: priorities.value.find(p => p.id === task.priorityId)
        }
      })

      return {
        ...state,
        tasks: stateTasks,
      }
    })

    setKanban(kanbanData)
  }

  watch(prioritiesFilter, async (newFilters, existingFilters) => {
    await loadKanban()
  })

  return {
    kanban,
    setKanban,
    tasksCount,
    members,
    setMembers,
    priorities,
    setPriorities,
    states,
    setStates,
    tasks,
    setTasks,
    loadKanban,
    prioritiesFilter
  }
})
