import { client } from './client'

export const taskCommentsAPI = (boardId, taskId) =>
  client.get(`/boards/${boardId}/tasks/${taskId}/comments`)
