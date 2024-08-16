<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { accountStatusAPI, setCSRFToken } from '@/utils/api'
import { onMounted, ref } from 'vue';
import { useUserStore } from '@/stores/user';
import Spinner from '@/components/base/Spinner.vue';

const userStore = useUserStore()
const loading = ref(false)

onMounted(async () => {
  try {
    loading.value = true
    const { data } = await accountStatusAPI()
    if(!data.isAuthenticated) {
      userStore.logoutUser()
      return
    }

    userStore.loginUser(data.loggedInUser)
    loading.value = false
  } catch (error) {
    console.log(error)
  }
})

const theme = {
  token: {
    fontSize: 13,
    borderRadius: 3,
    colorPrimary: '#6f5c92',
  },
}
</script>

<template>
  <a-config-provider :theme="theme">
    <a-flex align="center" justify="center" style="height: 100vh;" v-if="loading">
      <Spinner />
    </a-flex>
    <RouterView v-else />
  </a-config-provider>
</template>

<style scoped></style>
