<script setup>
import { ref } from 'vue'

const loginForm = ref({
  email: '',
  password: '',
})

const onFinish = (values) => {
    try {
        console.log(values)
    } catch (error) {
        console.log(error)
    }
}
</script>

<template>
  <a-flex justify="center" align="center" style="height: 90vh">
    <a-card size="small" style="width: 300px">
      <h2>Login</h2>
      <a-form layout="vertical" :model="loginForm" name="loginForm" hideRequiredMark @finish="onFinish">
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
          :rules="[{ required: true, message: 'Please input your password!' }]"
        >
          <a-input-password v-model:value="loginForm.password"></a-input-password>
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
