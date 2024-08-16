<script setup>
import { useUserStore } from '@/stores/user'
import { accountRegisterAPI, client, setCSRFToken } from '@/utils/api'
import { message } from 'ant-design-vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const registerForm = ref({
  email: '',
  first_name: '',
  last_name: '',
  password: '',
})

const onFinish = async (values) => {
  try {
    const { data } = await accountRegisterAPI(values)
    userStore.loginUser(data.user)

    // After Login CSRF Token changes, so we need to set csrf token again to our API Client
    setCSRFToken()

    // Redirect to home Page
    router.push({ name: 'index' })
  } catch (error) {
    message.warning(error.data.response.detail)
  }
}
</script>

<template>
  <a-flex justify="center" align="center" style="height: 90vh">
    <a-card size="small" style="width: 300px">
      <h2>Register</h2>
      <a-form
        layout="vertical"
        :model="registerForm"
        name="registerForm"
        hideRequiredMark
        @finish="onFinish"
      >
        <a-form-item
          label="Email"
          name="email"
          :rules="[{ required: true, message: 'Please input your email!' }]"
        >
          <a-input v-model:value="registerForm.email"></a-input>
        </a-form-item>

        <a-form-item
          label="First name"
          name="first_name"
          :rules="[
            { required: true, message: 'Please input your first_name!' },
          ]"
        >
          <a-input v-model:value="registerForm.first_name"></a-input>
        </a-form-item>

        <a-form-item label="Last name" name="last_name">
          <a-input v-model:value="registerForm.last_name"></a-input>
        </a-form-item>

        <a-form-item
          label="Password"
          name="password"
          :rules="[{ required: true, message: 'Please input your password!' }]"
        >
          <a-input-password
            v-model:value="registerForm.password"
          ></a-input-password>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit" style="width: 100%"
            >Submit</a-button
          >
        </a-form-item>
      </a-form>
    </a-card>
  </a-flex>
</template>
