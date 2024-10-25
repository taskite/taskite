<script setup>
import AccountSettingsLayout from '@/components/base/account-settings-layout.vue';
import { Button, Form, FormItem, InputPassword, message } from 'ant-design-vue';
import { ref } from 'vue';
import { handleResponseError } from '@/utils/helpers';
import { accountsPasswordChangeAPI } from '../../utils/api';

const passwordChangeForm = ref({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
})
const formRef = ref();

const onFinish = async (values) => {
    try {
        const { data } = await accountsPasswordChangeAPI(values)
        message.success(data.detail)
        window.location.href = "/"
    } catch (error) {
        handleResponseError(error)
    }
}
</script>

<template>
    <AccountSettingsLayout page="security">
        <div class="w-80">
            <div class="text-xl mb-2">Change password</div>
            <Form :model="passwordChangeForm" name="passwordChangeForm" layout="vertical" @finish="onFinish"
                hide-required-mark ref="formRef">
                <FormItem label="Current password" name="currentPassword"
                    :rules="[{ required: true, message: 'Please enter current password!' }]">
                    <InputPassword v-model:value="passwordChangeForm.currentPassword" />
                </FormItem>

                <FormItem label="New password" name="newPassword"
                    :rules="[{ required: true, message: 'Please enter new password!' }]">
                    <InputPassword v-model:value="passwordChangeForm.newPassword" />
                </FormItem>

                <FormItem label="Confirm password" name="confirmPassword"
                    :rules="[{ required: true, message: 'Please enter confirm password!' }]">
                    <InputPassword v-model:value="passwordChangeForm.confirmPassword" />
                </FormItem>

                <FormItem>
                    <Button type="primary" html-type="submit" class="mt-2">Change password</Button>
                </FormItem>
            </Form>
        </div>
    </AccountSettingsLayout>
</template>