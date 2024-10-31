import { client } from './client'

export const stateListAPI = (boardId) => client.get(`/boards/${boardId}/states`)

export const stateSequenceUpdateAPI = (boardId, stateId, updatedData) =>
  client.patch(
    `/boards/${boardId}/states/${stateId}/update-sequence`,
    updatedData
  )

export const stateCreateAPI = (boardId, data) =>
  client.post(`/boards/${boardId}/states`, data)

export const stateDeleteAPI = (boardId, stateId) =>
  client.delete(`/boards/${boardId}/states/${stateId}`)
