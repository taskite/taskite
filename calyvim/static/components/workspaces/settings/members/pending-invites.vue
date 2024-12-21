<script setup>
import { h } from 'vue';
import { Button, message, Table } from 'ant-design-vue';
import dayjs from 'dayjs';
import { DeleteOutlined, SendOutlined } from '@ant-design/icons-vue';
import { workspaceResendInviteAPI } from '@/utils/api';
import { handleResponseError } from '@/utils/helpers';

const props = defineProps(['workspaceId', 'invites', 'hasEditPermission'])
const emit = defineEmits(['remove'])

const resendInvitation = async (inviteId) => {
    try {
        const { data } = await workspaceResendInviteAPI(props.workspaceId, inviteId)
        message.success(data.detail)
    } catch (error) {
        handleResponseError(error)
    }
}

const columns = [
    {
        title: 'Email',
        key: 'email'
    },
    {
        title: 'Detail',
        key: 'detail'
    },
    {
        title: 'Actions',
        key: 'actions'
    }
]
</script>

<template>
    <Table :columns="columns" :dataSource="props.invites">
        <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'email'">
                <div>{{ record.email }}</div>
            </template>

            <template v-else-if="column.key === 'detail'">
                <div>{{ record.invitedBy.firstName }} invited on {{ dayjs(record.createdAt).format('D MMM YY') }}</div>
            </template>

            <template v-else-if="column.key === 'actions'">
                <div class="flex gap-1">
                    <Button type="text" :icon="h(SendOutlined)" :disabled="!props.hasEditPermission"
                        @click="resendInvitation(record.id)">Resend invitation</Button>
                    <Button type="text" :icon="h(DeleteOutlined)" danger :disabled="!props.hasEditPermission"
                        @click="emit('remove', record.id)">Delete invitation</Button>
                </div>
            </template>
        </template>
    </Table>
</template>