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
