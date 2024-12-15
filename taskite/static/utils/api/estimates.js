import { client } from './client'

export const estimateListAPI = (boardId) =>
  client.get(`/boards/${boardId}/estimates`)
