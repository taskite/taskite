<script setup>
import AccountsLayout from '@/components/base/accounts-layout.vue'
import { h, ref } from 'vue';
import { Button, Form, FormItem, Input, InputPassword, message } from 'ant-design-vue';
import { GithubOutlined, GoogleOutlined } from '@ant-design/icons-vue';
import { accountsLoginAPI } from '@/utils/api';

const loginForm = ref({
    email: '',
    password: ''
})

const loading = ref(false)

const onFinish = async (values) => {
    try {
        loading.value = true
        const { data } = await accountsLoginAPI(values)
        localStorage.setItem('currentUser', JSON.stringify(data.user))
        window.location.href = `/`
    } catch (error) {
        message.info(error?.response.data?.detail)
    } finally {
        loading.value = false
    }
}

</script>

<template>
    <AccountsLayout>
        <div class="flex items-center justify-center mb-4">
            <h1 class="text-2xl font-bold">Log In</h1>
        </div>

        <Form layout="vertical" :model="loginForm" name="loginForm" @finish="onFinish" hide-required-mark>
            <FormItem label="Email" name="email" :rules="[{ required: true, message: 'Please input your email!' }]">
                <Input v-model:value="loginForm.email" placeholder="alison@company.com" />
            </FormItem>

            <FormItem label="Password" name="password"
                :rules="[{ required: true, message: 'Please input a strong password!' }]">
                <template #extra>
                    <a class="text-primary hover:text-primary" href="/accounts/reset/">Forgot Password?</a>
                </template>
                <InputPassword v-model:value="loginForm.password" placeholder="***********" />
            </FormItem>

            <FormItem>
                <Button :loading="loading" type="primary" class="w-full" html-type="submit">Log in</Button>
            </FormItem>
        </Form>

        <p class="mt-4 text-center text-sm text-gray-600">
            Don't have an account?
            <a href="/accounts/register/" class="font-medium text-primary">Create an account</a>
        </p>

        <div class="mt-6">
            <div class="relative">
                <div class="absolute inset-0 flex items-center">
                    <div class="w-full border-t border-gray-300"></div>
                </div>
                <div class="relative flex justify-center text-sm">
                    <span class="px-2 bg-white text-gray-500">Or continue with</span>
                </div>
            </div>

            <div class="mt-6 grid grid-cols-2 gap-3">
                <Button :icon="h(GoogleOutlined)" ghost disabled>Google (beta)</Button>
                <Button :icon="h(GithubOutlined)" ghost disabled>Github (beta)</Button>
            </div>
        </div>
    </AccountsLayout>
</template>