<script setup>
import { useUserStore } from '@/stores/user'
import { accountResendVerification } from '@/utils/api';
import { message } from 'ant-design-vue';

const userStore = useUserStore()
const resendVerificationEmail = async () => {
    try {
        const { data } = await accountResendVerification()
        message.success(data.detail)
    } catch (error) {
        if(error?.response.status === 429) {
          message.warning('Please wait for sometime, before retrying to send another email.')

          return
        }

        message.error(error.response.data.detail)
    }
}
</script>

<template>
  <a-alert type="warning" banner v-if="!userStore.loggedInUser.isVerified">
    <template #message>
      <div>
        Please check your inbox to verify your email address
        <span class="font-semibold italic">{{
          userStore.loggedInUser.email
        }}</span
        >. If you haven't received the email, you can
        <a class="italic underline" @click="resendVerificationEmail">resend it</a>.
      </div>
    </template>
  </a-alert>
</template>
