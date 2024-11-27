import { client } from './client'

export const taskCommentsAPI = (boardId, taskId, commentType = 'all') =>
  client.get(`/boards/${boardId}/tasks/${taskId}/comments`, {
    params: {
      commentType,
    },
  })

export const taskCommentsCreateAPI = (boardId, taskId, data) =>
  client.post(`/boards/${boardId}/tasks/${taskId}/comments`, data)

export const taskCommentsLastAPI = (boardId, taskId) =>
  client.get(`/boards/${boardId}/tasks/${taskId}/comments/last`)

export const taskAttachmentsCreateAPI = (boardId, taskId, data) =>
  client.post(`/boards/${boardId}/tasks/${taskId}/attachments`, data)

export const taskAttachmentsListAPI = (boardId, taskId) =>
  client.get(`/boards/${boardId}/tasks/${taskId}/attachments`)
