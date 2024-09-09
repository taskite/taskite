<script setup>
import { useUserStore } from '@/stores/user'
import { accountRegisterAPI, client, setCSRFToken } from '@/utils/api'
import { message } from 'ant-design-vue'
import { ref } from 'vue'
import { useRouter, RouterLink, useRoute } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const registerForm = ref({
  email: route.query?.email || '',
  first_name: '',
  last_name: '',
  password: '',
  company: '',
})

const onFinish = async (values) => {
  try {
    const query = {
      inviteId: route.query?.inviteId,
    }

    const { data } = await accountRegisterAPI(values, query)
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
      <a-card size="small" class="w-96 px-2">
        <div class="text-2xl font-semibold mb-2 flex justify-center">
          Register
        </div>
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
            <a-input
              v-model:value="registerForm.email"
              :disabled="route.query?.email"
            ></a-input>
          </a-form-item>

          <a-row :gutter="12">
            <a-col :span="12">
              <a-form-item
                label="First name"
                name="first_name"
                :rules="[
                  { required: true, message: 'Please input your first name!' },
                ]"
              >
                <a-input v-model:value="registerForm.first_name"></a-input>
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item label="Last name" name="last_name">
                <a-input v-model:value="registerForm.last_name"></a-input>
              </a-form-item>
            </a-col>
          </a-row>

          <a-form-item
            label="Company"
            name="company"
          >
            <a-input v-model:value="registerForm.company"></a-input>
          </a-form-item>

          <a-form-item
            label="Password"
            name="password"
            :rules="[
              { required: true, message: 'Please input your password!' },
            ]"
          >
            <a-input-password
              v-model:value="registerForm.password"
            ></a-input-password>
          </a-form-item>
          <a-form-item>
            <a-button type="primary" html-type="submit" style="width: 100%"
              >Continue</a-button
            >
          </a-form-item>
        </a-form>

        <div class="flex justify-center mb-3">
          Already have an account? &nbsp<RouterLink :to="{ name: 'login' }"
            >Login</RouterLink
          >
        </div>
      </a-card>
    </a-flex>
  </div>
</template>
