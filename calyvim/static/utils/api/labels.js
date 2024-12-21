import { client } from './client'

export const labelListAPI = (boardId) => client.get(`/boards/${boardId}/labels`)