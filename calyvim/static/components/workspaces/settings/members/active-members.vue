<script setup>
import { Avatar, Button, message, Select, SelectOption, Table, Tag } from 'ant-design-vue';
import { generateAvatar } from '@/utils/helpers';
import dayjs from 'dayjs';
import { workspaceMembershipsUpdateAPI } from '@/utils/api';
import { h, ref } from 'vue';
import { CloseOutlined } from '@ant-design/icons-vue';
import { handleResponseError } from '@/utils/helpers';

const props = defineProps(['memberships', 'workspaceId', 'hasEditPermission'])
const emit = defineEmits(['remove'])

const columns = [
    {
        title: 'Name',
        key: 'name'
    },
    {
        title: 'Email',
        key: 'email'
    },
    {
        title: 'Role',
        key: 'role'
    },
    {
        title: 'Teams',
        key: 'teams'
    },
    {
        title: 'Joined',
        key: 'joined'
    },
    {
        title: 'Actions',
        key: 'actions'
    }
]

const loading = ref('')
const handleRoleChange = async (membershipId, newRole) => {
    try {
        loading.value = membershipId
        const updateData = {
            role: newRole
        }

        await workspaceMembershipsUpdateAPI(props.workspaceId, membershipId, updateData)
        message.success('Member role has been updated.')
    } catch (error) {
        handleResponseError(error)
    } finally {
        loading.value = ''
    }
}

const roleOptions = ref([
    {
        value: 'collaborator',
        label: 'Collaborator',
        description: 'Can view boards and content but cannot modify workspace settings.',
    },
    {
        value: 'maintainer',
        label: 'Maintainer',
        description: 'Can modify basic workspace settings, excluding critical actions like deletion or billing.',
    },
    {
        value: 'guest',
        label: 'Guest',
        description: 'Has limited access and can only view assigned items, such as specific boards or tasks, without the ability to make any modifications.'
    },
    {
        value: 'admin',
        label: 'Admin',
        description: 'Has full access to manage the workspace, including settings, members, and permissions.',
    },
])
</script>

<template>
    <Table :columns="columns" :dataSource="props.memberships" size="small">
        <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'name'">
                <div class="flex items-center gap-2">
                    <Avatar :src="record.user.avatar ? record.user.avatar : generateAvatar(record.user.firstName)" />
                    <div class="flex flex-col">
                        <div>
                            {{ record.user.firstName }} {{ record.user?.lastName }}
                        </div>
                        <div class="text-xs text-gray-500">@{{ record.user.username }}</div>
                    </div>
                </div>
            </template>

            <template v-else-if="column.key === 'email'">
                {{ record.user.email }}
            </template>

            <template v-else-if="column.key === 'role'">
                <Select v-model:value="record.role" style="width: 250px"
                    @change="(role) => handleRoleChange(record.id, role)" :disabled="!props.hasEditPermission"
                    :loading="loading === record.id" :options="roleOptions">
                    <template #option="{ value: val, label, description }">
                        <div class="flex flex-col gap-1">
                            <div class="font-semibold">{{ label }}</div>
                            <div class="text-xs text-wrap">{{ description }}</div>
                        </div>
                    </template>
                </Select>
            </template>

            <template v-else-if="column.key === 'teams'">
                <div v-if="record.user.teams.length === 0">-</div>
                <div v-else>
                    <Tag :bordered="false" v-for="team in record.user.teams" :key="team.id">{{ team.name }}
                    </Tag>
                </div>
            </template>

            <template v-else-if="column.key === 'joined'">
                {{ dayjs(record.createdAt).format('D MMM YY') }}
            </template>

            <template v-else-if="column.key === 'actions'">
                <div class="flex gap-2">
                    <Button type="text" :icon="h(CloseOutlined)" :disabled="!props.hasEditPermission" class="text-gray-500"
                        @click="emit('remove', record.id)">
                        Remove
                    </Button>
                </div>
            </template>
        </template>
    </Table>
</template>