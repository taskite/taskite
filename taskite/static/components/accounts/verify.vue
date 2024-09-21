<script setup>
import { MailOutlined, SendOutlined } from '@ant-design/icons-vue';
import BaseLayout from '@/components/base/base-layout.vue';
import { Button } from 'ant-design-vue';
import { h } from 'vue';
import { MailCheckIcon } from 'lucide-vue-next';
import { accountsResendVerificationEmailAPI } from '@/utils/api';

const handleResend = async () => {
    try {
        await accountsResendVerificationEmailAPI()
    } catch (error) {
        console.log(error)
    }
}
</script>

<template>
    <BaseLayout>
        <div class="min-h-screen bg-gray-100 flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8">
            <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-md">
                <div class="text-center">
                    <MailCheckIcon class="mx-auto h-12 w-12 text-primary" />
                    <h2 class="mt-6 text-3xl font-extrabold text-gray-900">Check your email</h2>
                    <p class="mt-2 text-sm text-gray-600">
                        We've sent a verification link to your email address. Please click the link to verify your
                        account.
                    </p>
                </div>
                <div class="mt-8 space-y-6">
                    <p class="text-center text-sm text-gray-500">
                        Didn't receive the email? Check your spam folder or try resending.
                    </p>
                    <div class="flex justify-center">
                        <Button type="primary" :icon="h(SendOutlined)" @click="handleResend">Resend</Button>
                    </div>
                </div>
            </div>
            <div class="mt-8 text-center">
                <p class="text-sm text-gray-600">
                    Need help? <a href="#" class="font-medium text-primary hover:text-primary-dark">Contact Support</a>
                </p>
            </div>
        </div>
    </BaseLayout>
</template>