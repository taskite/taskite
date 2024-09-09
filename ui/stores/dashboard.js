import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useDashboardStore = defineStore('dashboard', () => {
  const workspaces = ref([])
  const setWorkspaces = (workspacesData) => {
    workspaces.value = workspacesData
  }

  const boards = ref([])
  const setBoards = (boardsData) => {
    boards.value = boardsData
  }

  const getBoardsFromWorkspaceId = (workspaceId) => {
    return boards.value.filter((b) => b.workspaceId === workspaceId)
  }

  const allowedWorkspaces = computed(() => {
    return workspaces.value.filter(
      (workspace) => workspace?.membership.role === 'admin'
    )
  })

  const addBoard = (boardData) => {
    boards.value.push(boardData)
  }

  return {
    workspaces,
    setWorkspaces,
    boards,
    setBoards,
    addBoard,
    getBoardsFromWorkspaceId,
    allowedWorkspaces,
  }
})
