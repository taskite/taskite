<script setup>
import { Avatar, Button, message, Select, SelectOption, Table, Tag } from 'ant-design-vue';
import { generateAvatar } from '@/utils/helpers';
import dayjs from 'dayjs';
import { workspaceMembershipsUpdateAPI } from '@/utils/api';
import { h, ref } from 'vue';
import { CloseOutlined } from '@ant-design/icons-vue';

const props = defineProps(['memberships', 'notAdmin', 'workspaceId'])
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
        console.log(error)
    } finally {
        loading.value = ''
    }
}

</script>

<template>
    <Table :columns="columns" :dataSource="props.memberships" size="small">
        <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'name'">
                <div class="flex items-center gap-2">
                    <Avatar :src="generateAvatar(record.user.firstName)" />
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
                <Select v-model:value="record.role" style="width: 140px"
                    @change="(role) => handleRoleChange(record.id, role)" :disabled="props.notAdmin"
                    :loading="loading === record.id">
                    <SelectOption value="collaborator">Collaborator</SelectOption>
                    <SelectOption value="admin">Admin</SelectOption>
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
                    <Button type="text" :icon="h(CloseOutlined)" :disabled="props.notAdmin" class="text-gray-500"
                        @click="emit('remove', record.id)">
                        Remove
                    </Button>
                </div>
            </template>
        </template>
    </Table>
</template>