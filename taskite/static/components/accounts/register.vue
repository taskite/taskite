<script setup>
import { h, ref } from 'vue';
import BaseLayout from '@/components/base/base-layout.vue';
import { Button, Form, FormItem, Input, InputPassword, message } from 'ant-design-vue';
import { GithubOutlined, GoogleOutlined } from '@ant-design/icons-vue';
import { accountsRegisterAPI } from '../../utils/api';

const props = defineProps(['invitationId'])

const registerForm = ref({
    email: '',
    firstName: '',
    lastName: '',
    password: ''
})

const loading = ref(false)

const onFinish = async (values) => {
    try {
        loading.value = true

        if(!!props.invitationId) {
            values['invitationId'] = props.invitationId
        }
        
        const { data } = await accountsRegisterAPI(values)
        localStorage.setItem('currentUser', JSON.stringify(data.user))
        window.location.href = `/w`
    } catch (error) {
        message.info(error?.response.data?.detail)
    } finally {
        loading.value = false
    }
}

</script>

<template>
    <BaseLayout>
        <div class="min-h-screen flex items-center justify-center p-4 bg-gray-100">
            <div class="rounded-lg flex flex-col md:flex-row max-w-3xl w-full">
                <!-- Left side -->
                <div class="p-8 md:w-1/2 flex items-center justify-center">
                    <div class="text-center">
                        <div class="text-4xl mb-4">🦔</div>
                        <p class="text-xl font-semibold text-gray-800">Welcome to Taskite Cloud!</p>
                        <p class="mt-1 text-gray-600">Catch the productivity wind.</p>
                    </div>
                </div>

                <!-- Right side -->
                <div class="p-8 md:w-1/2 shadow-xl bg-white">
                    <div class="flex items-center justify-center mb-4">
                        <h1 class="text-2xl font-bold">Get started</h1>
                    </div>

                    <Form layout="vertical" :model="registerForm" name="registerForm" @finish="onFinish"
                        hide-required-mark>
                        <FormItem label="Email" name="email"
                            v-if="!!!props.invitationId"
                            :rules="[{ required: true, message: 'Please input your email!' }]">
                            <Input v-model:value="registerForm.email" placeholder="alison@company.com" />
                        </FormItem>

                        <div class="grid grid-cols-2 gap-2">
                            <FormItem label="First name" name="firstName"
                                :rules="[{ required: true, message: 'Please input your name!' }]">
                                <Input v-model:value="registerForm.firstName" placeholder="Alison" />
                            </FormItem>

                            <FormItem label="Last name" name="lastName">
                                <Input v-model:value="registerForm.lastName" placeholder="Stewart" />
                            </FormItem>
                        </div>

                        <FormItem label="Password" name="password"
                            :rules="[{ required: true, message: 'Please input a strong password!' }]">
                            <InputPassword v-model:value="registerForm.password" placeholder="***********" />
                        </FormItem>

                        <FormItem>
                            <Button :loading="loading" type="primary" class="w-full" html-type="submit">Continue</Button>
                        </FormItem>
                    </Form>

                    <p class="mt-4 text-center text-sm text-gray-600">
                        Already have an account account?
                        <a href="/accounts/login" class="font-medium text-primary">Log in</a>
                    </p>

                    <div class="mt-6" v-if="!!!props.invitationId">
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
                </div>
            </div>
        </div>
    </BaseLayout>
</template>