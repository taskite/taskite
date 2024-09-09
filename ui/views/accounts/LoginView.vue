<script setup>
import { useUserStore } from '@/stores/user'
import { accountLoginAPI, client, setCSRFToken } from '@/utils/api'
import { message } from 'ant-design-vue'
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const loginForm = ref({
  email: '',
  password: '',
})

const onFinish = async (values) => {
  try {
    const { data } = await accountLoginAPI(values)
    userStore.loginUser(data.user)

    // After Login CSRF Token changes, so we need to set csrf token again to our API Client
    setCSRFToken()

    // Redirect to home Page
    router.push({ name: 'home-index' })
  } catch (error) {
    message.warning(error.data.response.detail)
  }
}
</script>

<template>
  <div class="h-screen account-page">
    <a-flex justify="center" align="center" style="height: 90vh">
      <a-card size="small" class="px-2 w-80">
        <div class="text-2xl font-semibold mb-2 flex justify-center">Log In</div>
        <a-form
          layout="vertical"
          :model="loginForm"
          name="loginForm"
          hideRequiredMark
          @finish="onFinish"
        >
          <a-form-item
            label="Email"
            name="email"
            :rules="[{ required: true, message: 'Please input your email!' }]"
          >
            <a-input v-model:value="loginForm.email"></a-input>
          </a-form-item>

          <a-form-item
            label="Password"
            name="password"
            :rules="[
              { required: true, message: 'Please input your password!' },
            ]"
          >
            <a-input-password
              v-model:value="loginForm.password"
            ></a-input-password>
          </a-form-item>
          <a-form-item>
            <a-button type="primary" html-type="submit" style="width: 100%"
              >Continue</a-button
            >
          </a-form-item>
        </a-form>

        <div class="flex justify-center mb-3">
          Don't have an account? &nbsp<RouterLink :to="{ name: 'register' }">Register</RouterLink>
        </div>
      </a-card>
    </a-flex>
  </div>
</template>

<style>
</style>
