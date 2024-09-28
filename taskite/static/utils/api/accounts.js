import { client } from './client'

export const accountsLoginAPI = (data) => client.post('/accounts/login', data)

export const accountsRegisterAPI = (data) => client.post('/accounts/register', data)

export const accountsResendVerificationEmailAPI = () => client.post('/accounts/resend-verification')

export const accountsProfileAPI = () => client.get(`/accounts/profile`)

export const accountsProfileUpdateAPI = (data) => client.patch(`/accounts/profile`, data)