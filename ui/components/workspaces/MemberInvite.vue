<script setup>
import { workspaceInviteCreateAPI } from '@/utils/api';
import { SendOutlined } from '@ant-design/icons-vue'
import { h, ref } from 'vue'

const props = defineProps(['workspaceId'])
const emit = defineEmits(['invited'])

const formRef = ref();
const inviteForm = ref({
  emails: '',
})

const finishInviteForm = async (values) => {
  const formData = {
    emails: values.emails.split(','),
  }

  try {
    const { data } = await workspaceInviteCreateAPI(props.workspaceId, formData)
    emit('invited', data)
    formRef.value.resetFields()
  } catch (error) {
    console.log(error)
  }
}
</script>

<template>
  <a-form :model="inviteForm" layout="vertical" @finish="finishInviteForm" ref="formRef">
    <a-form-item label="Emails" name="emails">
      <a-textarea :rows="4" v-model:value="inviteForm.emails"> </a-textarea>
      <div class="text-sm text-slate-500">
        Use comma seprated values for multiple emails.
      </div>
    </a-form-item>

    <a-form-item>
      <a-button class="w-full" html-type="submit" :icon="h(SendOutlined)"
        >Invite</a-button
      >
    </a-form-item>
  </a-form>
</template>
