import { client } from './client'

export const workspaceMemberSearchAPI = (workspaceId, searchQuery) =>
  client.get(`/workspaces/${workspaceId}/members/search`, {
    params: {
      q: searchQuery,
    },
  })

export const workspaceMembershipsAPI = (workspaceId) =>
  client.get(`/workspaces/${workspaceId}/memberships`)

export const workspaceTeamsAPI = (workspaceId) =>
  client.get(`/workspaces/${workspaceId}/teams`)

export const workspaceTeamCreateAPI = (workspaceId, data) =>
  client.post(`/workspaces/${workspaceId}/teams`, data)

export const workspaceTeamDeleteAPI = (workspaceId, teamId) =>
  client.delete(`/workspaces/${workspaceId}/teams/${teamId}`)

export const workspaceTeamMembershipsAPI = (workspaceId, teamId) =>
  client.get(`/workspaces/${workspaceId}/team_memberships`, {
    params: {
      teamId,
    },
  })

export const workspaceTeamMembershipsCreateAPI = (workspaceId, data) =>
  client.post(`/workspaces/${workspaceId}/team_memberships`, data)

export const workspaceTeamMembershipsDeleteAPI = (workspaceId, membershipId) =>
  client.delete(`/workspaces/${workspaceId}/team_memberships/${membershipId}`)
