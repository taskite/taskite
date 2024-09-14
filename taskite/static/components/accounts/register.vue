<script setup>
import { Card, Flex, Form, Input, Button, message } from 'ant-design-vue'
import { h, ref } from 'vue'

import BaseLayout from '@/components/base/base-layout.vue'
import { UserOutlined } from '@ant-design/icons-vue';
import { accountsRegisterAPI } from '@/utils/api';

const props = defineProps(['next'])
const registerForm = ref({
    email: '',
    firstName: '',
    lastName: '',
    password: '',
    company: '',
})
// State for loading and error
const loading = ref(false)
const error = ref('')

const onFinish = async (values) => {
    try {
        loading.value = true
        await accountsRegisterAPI(values)
        message.success('Register successfull!')
        window.location.href = "/"
    } catch (err) {
        error.value = err.response?.data?.message || 'Register failed'
        message.error(error.value)
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <BaseLayout>
        <Flex justify="center" align="center" style="height: 90vh">
            <Card size="small" class="register-card">
                <Flex class="title" justify="center" align="center">Log In</Flex>
                <Form layout="vertical" :model="registerForm" name="registerForm" hideRequiredMark @finish="onFinish">
                    <Form.Item label="Email" name="email"
                        :rules="[{ required: true, message: 'Please input your email!' }]">
                        <Input v-model:value="registerForm.email"></Input>
                    </Form.Item>

                    <Form.Item label="First name" name="firstName"
                        :rules="[{ required: true, message: 'Please input your first name!' }]">
                        <Input v-model:value="registerForm.firstName"></Input>
                    </Form.Item>

                    <Form.Item label="Last name" name="lastName">
                        <Input v-model:value="registerForm.lastName"></Input>
                    </Form.Item>

                    <Form.Item label="Company" name="company">
                        <Input v-model:value="registerForm.company"></Input>
                    </Form.Item>

                    <Form.Item label="Password" name="password" :rules="[
                        { required: true, message: 'Please input your password!' },
                    ]">
                        <Input.Password v-model:value="registerForm.password"></Input.Password>
                    </Form.Item>

                    <Form.Item>
                        <Button html-type="submit" type="primary" class="full-button"
                            :icon="h(UserOutlined)">Register</Button>
                    </Form.Item>
                </Form>
            </Card>
        </Flex>
    </BaseLayout>
</template>

<style scoped>
.title {
    font-size: larger;
    font-weight: bold;
}

.register-card {
    width: 300px;
}

.full-button {
    width: 100%;
}
</style>
