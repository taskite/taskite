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

  const estimates = ref([])
  const setEstimates = (estimatesData) => {
    estimates.value = estimatesData
  }

  const sprints = ref([])
  const setSprints = (sprintsData) => {
    sprints.value = sprintsData
    const activeSprint = sprintsData.find((sprint) => sprint.isActive === true)
    if (!!activeSprint) {
      sprintFilters.value = [activeSprint.id]
    }
  }

  const activeSprint = computed(() => {
    if (sprints.value.length === 0) {
      return null
    }

    return sprints.value.find((sprint) => sprint.isActive === true)
  })

  const assigneeFilters = ref([])
  const taskTypes = ref([])
  const priorityFilters = ref([])
  const labelFilters = ref([])
  const estimateFilters = ref([])
  const sprintFilters = ref([])

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

  const removeTask = (taskId) => {
    const task = tasks.value.find((task) => task.id === taskId)
    if (!task) return false

    const state = kanban.value.find((state) => state.id === task.stateId)
    if (!state) return false

    state.tasks = state.tasks.filter((task) => task.id !== taskId)
    tasks.value = tasks.value.filter((task) => task.id !== taskId)
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

  const selectedTask = ref('')
  const setSelectedTask = (taskId) => {
    selectedTask.value = taskId
  }

  const setSprintFilters = (sprintIds) => {
    sprintFilters.value = sprintIds
  }

  return {
    states,
    setStates,
    tasks,
    setTasks,
    removeTask,
    setupKanban,
    kanban,
    members,
    setMembers,
    priorities,
    setPriorities,
    labels,
    setLabels,
    estimates,
    setEstimates,
    sprints,
    setSprints,
    activeSprint,
    assigneeFilters,
    taskTypes,
    priorityFilters,
    labelFilters,
    estimateFilters,
    sprintFilters,
    setSprintFilters,
    addNewTask,
    updateTask,
    updateTaskState,
    selectedTask,
    setSelectedTask,
  }
})
