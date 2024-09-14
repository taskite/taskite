import { client } from './client'

export const accountsLoginAPI = (data) => client.post('/accounts/login', data)

export const accountsRegisterAPI = (data) => client.post('/accounts/register', data)