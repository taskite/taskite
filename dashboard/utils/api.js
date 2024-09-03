import applyCaseMiddleware from 'axios-case-converter'
import axios from 'axios'
import Cookies from 'js-cookie'

const options = {
  preservedKeys: [],
  ignoreHeaders: true,
}

export const client = applyCaseMiddleware(
  axios.create({
    baseURL: '/api',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken'),
    },
  }),
  options
)

export const setCSRFToken = () => {
  client.defaults.headers['X-CSRFToken'] = Cookies.get('csrftoken')
}

export const accountLoginAPI = (data) => client.post('/accounts/login', data)
export const accountRegisterAPI = (data, query) =>
  client.post('/accounts/register', data, {
    params: {
      ...query,
    },
  })
export const accountStatusAPI = () => client.get('/accounts/status')
export const accountLogoutAPI = () => client.get('/accounts/logout')
export const accountResendVerification = () => client.post('/accounts/resend-verification')

export const organizationListAPI = () => client.get('/organizations')
export const organizationListWithUserInfoAPI = () =>
  client.get('/organizations/with-user-info')
export const organizationPermissionsAPI = () =>
  client.get('/organizations/permissions')

export const workspaceListAPI = () => client.get('/workspaces')
export const workspaceMembershipsAPI = () =>
  client.get('/workspaces/memberships')
export const workspaceDetailAPI = (workspaceId) =>
  client.get(`/workspaces/${workspaceId}`)

export const workspaceMembershipListAPI = (workspaceId) =>
  client.get(`/workspaces/${workspaceId}/memberships`)

export const workspaceInviteListAPI = (workspaceId) =>
  client.get(`/workspaces/${workspaceId}/invites`)
export const workspaceInviteCreateAPI = (workspaceId, data) =>
  client.post(`/workspaces/${workspaceId}/invites`, data)

export const teamListAPI = (workspaceId) =>
  client.get(`/workspaces/${workspaceId}/teams`)

export const createBoardAPI = (data) => client.post('/boards', data)
export const boardListAPI = () => client.get('/boards')
export const boardMembershipsAPI = () => client.get('/boards/memberships')
export const boardMembershipAPI = (boardId) =>
  client.get(`/boards/${boardId}/membership`)
export const boardMembersAPI = (boardId) =>
  client.get(`/boards/${boardId}/members`)
export const boardDetailAPI = (boardId) => client.get(`/boards/${boardId}`)

export const stateListAPI = (boardId) => client.get(`/boards/${boardId}/states`)

export const priorityListAPI = (boardId) =>
  client.get(`/boards/${boardId}/priorities`)

export const taskListAPI = (boardId) => client.get(`/boards/${boardId}/tasks`)
