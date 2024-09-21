import { client } from './client'

export const boardListAPI = (workspaceId) =>
  client.get(`/boards`, {
    params: {
      workspaceId,
    },
  })

export const boardCreateAPI = (data) => client.post(`/boards`, data)

export const stateListAPI = (boardId) => client.get(`/boards/${boardId}/states`)

export const taskListAPI = (boardId) => client.get(`/boards/${boardId}/tasks`)

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
