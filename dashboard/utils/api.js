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

export const accountRegisterAPI = (data) =>
  client.post('/accounts/register', data)

export const accountStatusAPI = () => client.get('/accounts/status')

export const accountLogoutAPI = () => client.get('/accounts/logout')

export const organizationListAPI = () => client.get('/organizations')