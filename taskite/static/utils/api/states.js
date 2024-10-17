import { client } from './client'

export const stateListAPI = (boardId) => client.get(`/boards/${boardId}/states`) 