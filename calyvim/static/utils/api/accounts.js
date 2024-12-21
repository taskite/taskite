import { client } from './client'

export const accountsLoginAPI = (data) => client.post('/accounts/login', data)

export const accountsRegisterAPI = (data) => client.post('/accounts/register', data)

export const accountsResendVerificationEmailAPI = () => client.post('/accounts/resend-verification')

export const accountsProfileAPI = () => client.get(`/accounts/profile`)

export const accountsProfileUpdateAPI = (data) => client.patch(`/accounts/profile`, data)

export const accountsPasswordResetAPI = (data) => client.post(`/accounts/password-reset`, data)

export const accountsPasswordResetConfirmAPI = (data) => client.post('/accounts/password-reset-confirm', data)

export const accountsPasswordChangeAPI = (data) => client.post(`/accounts/password-change`, data)