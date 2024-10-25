<script setup>
import { ref } from 'vue';
import AccountsLayout from '@/components/base/accounts-layout.vue';
import { Button, Form, FormItem, Input, InputPassword, message } from 'ant-design-vue';
import { accountsPasswordResetConfirmAPI } from '@/utils/api';

const props = defineProps(['passwordResetId'])

const passwordResetConfirmForm = ref({
    passwordResetId: props.passwordResetId,
    newPassword: '',
    confirmPassword: ''
})

const rules = ref({
    newPassword: [
        {
            required: true,
            message: 'Please enter your new password',
            trigger: 'blur'
        },
        {
            min: 6,
            message: 'Password must be at least 6 characters long',
            trigger: 'blur'
        }
    ],
    confirmPassword: [
        {
            required: true,
            message: 'Please confirm your password',
            trigger: 'blur'
        },
        {
            validator: (rule, value) => {
                if (!value) {
                    return Promise.reject('Please confirm your password');
                } else if (value !== passwordResetConfirmForm.value.newPassword) {
                    return Promise.reject('Passwords do not match');
                } else {
                    return Promise.resolve();
                }
            },
            trigger: 'blur'
        }
    ]
});

const onFinish = async (values) => {
    try {
        const { data } = await accountsPasswordResetConfirmAPI(values)
        localStorage.setItem('currentUser', JSON.stringify(data.user))
        window.location.href = `/`
    } catch (error) {
        
    }
}
</script>

<template>
    <AccountsLayout>
        <div class="flex items-center justify-center mb-4">
            <h1 class="text-xl font-bold">Reset Password</h1>
        </div>

        <Form :model="passwordResetConfirmForm" name="passwordResetConfirm" layout="vertical" hide-required-mark
            :rules="rules" @finish="onFinish">
            <FormItem name="passwordResetId" class="hidden">
                <Input v-model:value="passwordResetConfirmForm.passwordResetId" />
            </FormItem>

            <FormItem label="New password" name="newPassword">
                <InputPassword v-model:value="passwordResetConfirmForm.newPassword" />
            </FormItem>

            <FormItem label="Confirm password" name="confirmPassword">
                <InputPassword v-model:value="passwordResetConfirmForm.confirmPassword" />
            </FormItem>

            <FormItem>
                <Button type="primary" html-type="submit" class="w-full">Reset password</Button>
            </FormItem>
        </Form>
    </AccountsLayout>
</template>