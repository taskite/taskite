<script setup>
import { useUserStore } from '@/stores/user'
import { accountLogoutAPI, setCSRFToken } from '@/utils/api'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router';

const userStore = useUserStore()
const router = useRouter()

const logoutUser = async () => {
  try {
    await accountLogoutAPI()
    userStore.logoutUser()
    setCSRFToken()

    router.push({ name: 'login' })
  } catch (error) {
    console.log(error)
  }
}

onMounted(async () => {
  await logoutUser()
})
</script>

<template></template>
