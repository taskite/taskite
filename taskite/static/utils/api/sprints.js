import { client } from './client'

export const sprintListAPI = (boardId) =>
  client.get(`/boards/${boardId}/sprints`)
