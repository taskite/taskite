import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const loggedInUser = ref(null)

  const loginUser = (userData) => {
    localStorage.setItem('loggedInUser', JSON.stringify(userData))
    loggedInUser.value = userData
  }

  const logoutUser = () => {
    localStorage.removeItem('loggedInUser')
    loggedInUser.value = null
  }

  const isAuthenticated = !!loggedInUser.value

  return { loggedInUser, loginUser, logoutUser, isAuthenticated }
})
