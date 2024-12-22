import { client } from './client'

export const sprintListAPI = (boardId) =>
  client.get(`/boards/${boardId}/sprints`)

export const sprintCreateAPI = (boardId, data) =>
  client.post(`/boards/${boardId}/sprints`, data)
