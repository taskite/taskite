import { client } from './client'

export const newslineListAPI = async (workspaceId) =>
  client.get(`/newslines`, {
    params: {
      workspaceId,
    },
  })
