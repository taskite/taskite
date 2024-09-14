import { client } from './client'

export const workspaceMembershipsAPI = (workspaceId) =>
  client.get(`/workspaces/${workspaceId}/memberships`)
