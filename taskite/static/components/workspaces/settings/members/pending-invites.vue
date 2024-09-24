<script setup>
import { h, onMounted, ref } from 'vue';
import { workspaceInvitesAPI } from '@/utils/api';
import { Button, Table } from 'ant-design-vue';
import dayjs from 'dayjs';
import { DeleteOutlined, SendOutlined } from '@ant-design/icons-vue';
import { workspaceResendInviteAPI } from '../../../../utils/api';

const props = defineProps(['workspaceId', 'notAdmin'])

const invites = ref([])
const loadWorkspaceInvites = async () => {
    try {
        const { data } = await workspaceInvitesAPI(props.workspaceId)
        invites.value = data.map((i) => {
            return {
                key: i.id,
                ...i
            }
        })
    } catch (error) {
        console.log(error)
    }
}

const resendInvitation = async (inviteId) => {
    try {
        await workspaceResendInviteAPI(props.workspaceId, inviteId)
    } catch (error) {
        console.log(error)
    }
}

onMounted(() => {
    loadWorkspaceInvites()
})

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
    <Table :columns="columns" :dataSource="invites">
        <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'email'">
                <div>{{ record.email }}</div>
            </template>

            <template v-else-if="column.key === 'detail'">
                <div>{{ record.invitedBy.firstName }} invited on {{ dayjs(record.createdAt).format('D MMM YY') }}</div>
            </template>

            <template v-else-if="column.key === 'actions'">
                <div class="flex gap-1">
                    <Button type="text" :icon="h(SendOutlined)" :disabled="notAdmin"
                        @click="resendInvitation(record.id)">Resend invitation</Button>
                    <Button type="text" :icon="h(DeleteOutlined)" danger :disabled="notAdmin">Delete invitation</Button>
                </div>
            </template>
        </template>
    </Table>
</template>