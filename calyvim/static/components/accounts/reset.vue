<script setup>
import AccountsLayout from '@/components/base/accounts-layout.vue';
import { Button, Form, FormItem, Input, message } from 'ant-design-vue';
import { ref } from 'vue';
import { accountsPasswordResetAPI } from '@/utils/api';
import { handleResponseError } from '@/utils/helpers';

const passwordResetForm = ref({
    email: ''
})

const onFinish = async (values) => {
    try {
        const { data } = await accountsPasswordResetAPI(values)
        message.success(data.detail)
    } catch (error) {
        handleResponseError(error)
    }
}
</script>

<template>
    <AccountsLayout>
        <div class="flex items-center justify-center mb-4">
            <h1 class="text-xl font-bold">Reset Password</h1>
        </div>

        <Form layout="vertical" @finish="onFinish" hide-required-mark :model="passwordResetForm"
            name="passwordResetForm">
            <FormItem label="Email" name="email" :rules="[{ required: true, message: 'Please enter email address.' }]">
                <Input v-model:value="passwordResetForm.email" />
            </FormItem>

            <FormItem>
                <Button type="primary" class="w-full" html-type="submit">Send reset email</Button>
            </FormItem>
        </Form>
    </AccountsLayout>
</template>