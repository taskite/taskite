<script setup>
import { MailOutlined, SendOutlined } from '@ant-design/icons-vue'
import BaseLayout from '@/components/base/base-layout.vue'
import { Button, message } from 'ant-design-vue'
import { h } from 'vue'
import { MailCheckIcon } from 'lucide-vue-next'
import { accountsResendVerificationEmailAPI } from '@/utils/api'
import { handleResponseError, generateAvatar, notify } from '@/utils/helpers'

const props = defineProps(['currentUser'])

const handleResend = async () => {
  try {
    const { data } = await accountsResendVerificationEmailAPI()
    notify('SEND', data.detail)
  } catch (error) {
    handleResponseError(error)
  }
}
</script>

<template>
  <BaseLayout>
    <div
      class="min-h-screen bg-gray-100 flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8"
    >
      <!-- User info and logout in top right corner -->
      <div class="absolute top-4 right-4 flex items-center space-x-4">
        <div class="flex items-center space-x-2">
          <div class="text-right">
            <div class="text-sm font-medium text-gray-900">
              {{ props.currentUser?.firstName }}
              {{ props.currentUser?.lastName }}
            </div>
            <div class="text-xs text-gray-500">
              {{ props.currentUser?.email }}
            </div>
            <div class="mt-1">
              <a
                class="text-xs cursor-pointer underline underline-offset-2"
                href="/app/accounts/logout/"
                >Logout</a
              >
            </div>
          </div>
          <Avatar
            :src="
              currentUser?.avatar
                ? currentUser.avatar
                : generateAvatar(currentUser?.firstName)
            "
            alt="Profile"
          />
        </div>
      </div>
      <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-md">
        <div class="text-center">
          <MailCheckIcon class="mx-auto h-12 w-12 text-primary" />
          <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
            Check your email
          </h2>
          <p class="mt-2 text-sm text-gray-600">
            We've sent a verification link to your email address. Please click
            the link to verify your account.
          </p>
        </div>
        <div class="mt-8 space-y-6">
          <p class="text-center text-sm text-gray-500">
            Didn't receive the email? Check your spam folder or try resending.
          </p>
          <div class="flex justify-center">
            <Button type="primary" :icon="h(SendOutlined)" @click="handleResend"
              >Resend</Button
            >
          </div>
        </div>
      </div>
      <div class="mt-8 text-center">
        <p class="text-sm text-gray-600">
          Need help?
          <a href="#" class="font-medium text-primary hover:text-primary-dark"
            >Contact Support</a
          >
        </p>
      </div>
    </div>
  </BaseLayout>
</template>
