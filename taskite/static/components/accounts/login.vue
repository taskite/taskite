<script setup>
import { Card, Flex, Form, Input, Button, message } from 'ant-design-vue'
import { h, ref } from 'vue'

import BaseLayout from '@/components/base/base-layout.vue'
import { UserOutlined } from '@ant-design/icons-vue';
import { accountsLoginAPI } from '@/utils/api';

const props = defineProps(['next'])
const loginForm = ref({
    email: '',
    password: '',
})
// State for loading and error
const loading = ref(false)
const error = ref('')

const onFinish = async (values) => {
    try {
        loading.value = true
        await accountsLoginAPI(values)
        message.success('Login successfull!')
        window.location.href = props.next
    } catch (err) {
        error.value = err.response?.data?.message || 'Login failed'
        message.error(error.value)
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <BaseLayout>
        <Flex justify="center" align="center" style="height: 90vh">
            <Card size="small" class="login-card">
                <Flex class="title" justify="center" align="center">Log In</Flex>
                <Form layout="vertical" :model="loginForm" name="loginForm" hideRequiredMark @finish="onFinish">
                    <Form.Item label="Email" name="email"
                        :rules="[{ required: true, message: 'Please input your email!' }]">
                        <Input v-model:value="loginForm.email"></Input>
                    </Form.Item>

                    <Form.Item label="Password" name="password" :rules="[
                        { required: true, message: 'Please input your password!' },
                    ]">
                        <Input.Password v-model:value="loginForm.password"></Input.Password>
                    </Form.Item>

                    <Form.Item>
                        <Button html-type="submit" type="primary" class="full-button"
                            :icon="h(UserOutlined)">Login</Button>
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

.login-card {
    width: 300px;
}

.full-button {
    width: 100%;
}
</style>
