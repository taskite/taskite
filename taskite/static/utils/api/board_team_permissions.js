import { client } from './client'

export const boardTeamPermissionCreateAPI = (boardId, data) =>
  client.post(`/boards/${boardId}/team_permissions`, data)

export const boardTeamPermissionListAPI = (boardId) =>
  client.get(`/boards/${boardId}/team_permissions`)

export const boardTeamPermissionUpdateAPI = (boardId, permissionId, data) =>
  client.patch(`/boards/${boardId}/team_permissions/${permissionId}`, data)

export const boardTeamPermissionDeleteAPI = (boardId, permissionId) =>
  client.delete(`/boards/${boardId}/team_permissions/${permissionId}`)
