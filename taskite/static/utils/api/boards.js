import { client } from './client'

export const boardListAPI = (workspaceId) =>
  client.get(`/boards`, {
    params: {
      workspaceId,
    },
  })
export const boardCreateAPI = (data) => client.post(`/boards`, data)
export const boardDetailAPI = (boardId) => client.get(`/boards/${boardId}`)
export const boardUpdateAPI = (boardId, data) =>
  client.patch(`/boards/${boardId}`, data)
export const boardMembersListAPI = (boardId) =>
  client.get(`/boards/${boardId}/members`)

export const stateListAPI = (boardId) => client.get(`/boards/${boardId}/states`)

export const taskListAPI = (boardId, filters = {}) =>
  client.get(`/boards/${boardId}/tasks`, {
    params: filters,
  })
export const taskCreateAPI = (boardId, data) =>
  client.post(`/boards/${boardId}/tasks`, data)
export const taskUpdateSequence = (boardId, taskId, data) =>
  client.patch(`/boards/${boardId}/tasks/${taskId}/update-sequence`, data)
export const taskUpdateAPI = (boardId, taskId, data) =>
  client.patch(`/boards/${boardId}/tasks/${taskId}`, data)
export const taskDetailAPI = (boardId, taskId) =>
  client.get(`/boards/${boardId}/tasks/${taskId}`)

export const priorityListAPI = (boardId) =>
  client.get(`/boards/${boardId}/priorities`)

export const boardMembershipsAPI = (boardId) =>
  client.get(`/boards/${boardId}/memberships`)
export const boardMembershipsCreateAPI = (boardId, data, membershipType) =>
  client.post(`/boards/${boardId}/memberships`, data, {
    params: {
      membershipType,
    },
  })

export const boardMembershipsDeleteAPI = (boardId, membershipId) =>
  client.delete(`/boards/${boardId}/memberships/${membershipId}`)

export const boardMembershipsUpdateAPI = (boardId, membershipId, updateData) =>
  client.patch(`/boards/${boardId}/memberships/${membershipId}`, updateData)
