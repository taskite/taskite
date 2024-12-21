import { client } from './client'

export const boardPermissionListAPI = (boardId) =>
  client.get(`/boards/${boardId}/permissions`)

export const boardPermissionCreateAPI = (boardId, data) =>
  client.post(`/boards/${boardId}/permissions`, data)

export const boardPermissionUpdateAPI = (boardId, permissionId, data) =>
  client.patch(`/boards/${boardId}/permissions/${permissionId}`, data)

export const boardPermissionDeleteAPI = (boardId, permissionId) =>
  client.delete(`/boards/${boardId}/permissions/${permissionId}`)
