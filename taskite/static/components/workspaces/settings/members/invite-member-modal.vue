<script setup>
import { UserAddOutlined } from '@ant-design/icons-vue';
import { Button, Form, FormItem, Textarea } from 'ant-design-vue';
import isEmail from 'validator/lib/isEmail';
import { h, ref } from 'vue';
import { workspaceMembersInviteAPI } from '@/utils/api';

const inviteForm = ref({
    emails: '',
    role: 'collaborator'
})
const formRef = ref();

const props = defineProps(['workspaceId'])
const emit = defineEmits(['invited'])

const onFinish = async (values) => {
    const emails = values['emails'].split(',').map(email => email.trim()).filter(email => {
        return isEmail(email)
    })

    try {
        const postData = {
            'emails': emails,
            'role': 'collaborator'
        }

        const { data } = await workspaceMembersInviteAPI(props.workspaceId, postData)
        const newInvites = data.map(i => {
            return {
                key: i.id,
                ...i
            }
        })

        // Reset the form
        formRef.value.resetFields()

        emit('invited', newInvites)
    } catch (error) {
        console.log(error)
    }
}
</script>

<template>
    <Form layout="vertical" :model="inviteForm" name="inviteForm" hide-required-mark @finish="onFinish" ref="formRef">
        <FormItem label="Emails" :rules="[{ required: true, message: 'Please enter emails' }]" name="emails">
            <Textarea v-model:value="inviteForm.emails" :rows="3" />
            <div class="text-xs text-gray-400">You can enter multiple email addresses, separated by commas.</div>
        </FormItem>

        <FormItem>
            <Button html-type="submit" type="primary" :icon="h(UserAddOutlined)">Send invitation</Button>
        </FormItem>
    </Form>
</template>