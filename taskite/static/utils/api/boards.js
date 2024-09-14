import { client } from './client'

export const boardListAPI = (workspaceId) => client.get(`/boards`, {
    params: {
        workspaceId
    }
})