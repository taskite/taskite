import { client } from './client'

export const taskCommentsAPI = (boardId, taskId, commentType = 'all') =>
  client.get(`/boards/${boardId}/tasks/${taskId}/comments`, {
    params: {
      commentType,
    },
  })

export const taskCommentsLastAPI = (boardId, taskId) =>
  client.get(`/boards/${boardId}/tasks/${taskId}/comments/last`)
