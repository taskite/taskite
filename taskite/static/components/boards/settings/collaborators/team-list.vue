<script setup>
import { computed, h, onMounted, ref } from 'vue';
import { Avatar, Select, SelectOption, Table, Button, Modal, message } from 'ant-design-vue';
import { generateAvatar, handleResponseError } from '@/utils/helpers';
import dayjs from 'dayjs';
import { CloseOutlined, UsergroupAddOutlined } from '@ant-design/icons-vue';
import AddTeamModal from './add-team-modal.vue';
import { boardTeamPermissionUpdateAPI, boardTeamPermissionListAPI, boardTeamPermissionDeleteAPI } from '@/utils/api';

const props = defineProps(['boardId', 'workspaceId', 'hasEditPermission'])

const permissions = ref([])
const loadBoardTeamPermissions = async () => {
    try {
        const { data } = await boardTeamPermissionListAPI(props.boardId)
        permissions.value = data.map(p => {
            return {
                ...p,
                key: p.id
            }
        })
    } catch (error) {
        handleResponseError(error)
    }
}

onMounted(() => {
    loadBoardTeamPermissions()
})

const columns = [
    {
        title: 'Team',
        key: 'team'
    },
    {
        title: 'Role',
        key: 'role'
    },
    {
        title: 'Joined',
        key: 'joined'
    },
    {
        // title: 'Action',
        key: 'action'
    }
]

const handleRoleChange = async (permissionId, role) => {
    try {
        const updateData = {
            role: role
        }
        await boardTeamPermissionUpdateAPI(props.boardId, permissionId, updateData)
        message.success('Board team permission updated successfully.')
    } catch (error) {
        handleResponseError(error)
    }
}

const deleteTeamPermission = async (permissionId) => {
    try {
        await boardTeamPermissionDeleteAPI(props.boardId, permissionId)
        permissions.value = permissions.value.filter(permission => permission.id !== permissionId)
        message.success('Team permission has been removed')
    } catch (error) {
        handleResponseError(error)
    }
}

const openTeamAddModal = ref(false)
const showTeamAddModal = () => {
    openTeamAddModal.value = true
}
const teams = computed(() => {
    return permissions.value.map(permission => permission.team)
})
const addPermissions = (data) => {
    permissions.value.push(data)
}

const roleOptions = ref([
    {
        value: 'collaborator',
        label: 'Collaborator',
        description: 'Can view boards and their content but cannot make changes to board settings.',
    },
    {
        value: 'maintainer',
        label: 'Maintainer',
        description: 'Can manage tasks and basic board settings, excluding critical actions like deleting the board or archiving it.',
    },
    {
        value: 'guest',
        label: 'Guest',
        description: 'Has restricted access, able only to view specific assigned boards or tasks without permission to make any modifications.',
    },
    {
        value: 'admin',
        label: 'Admin',
        description: 'Has full control over board settings, tasks, and member permissions on all assigned boards.',
    },
])
</script>

<template>
    <div class="flex justify-end mb-4">
        <Button :icon="h(UsergroupAddOutlined)" type="primary" @click="showTeamAddModal"
            :disabled="!props.hasEditPermission">Add team</Button>
    </div>
    <Table :columns="columns" :data-source="permissions">
        <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'team'">
                <div class="flex gap-1 items-center">
                    <Avatar :src="!!record.team.avatar ? record.team.avatar : generateAvatar(record.team.name, 5)"
                        shape="square" />
                    <div>{{ record.team.name }}</div>
                </div>
            </template>

            <template v-else-if="column.key === 'role'">
                <Select v-model:value="record.role" style="width: 220px"
                    @change="(role) => handleRoleChange(record.id, role)" :disabled="!props.hasEditPermission"
                    :options="roleOptions">
                    <template #option="{ value: val, label, description }">
                        <div class="flex flex-col gap-1">
                            <div class="font-semibold">{{ label }}</div>
                            <div class="text-xs text-wrap">{{ description }}</div>
                        </div>
                    </template>
                </Select>
            </template>

            <template v-else-if="column.key === 'joined'">
                <div>{{ dayjs(record.createdAt).format('MMMM D, YYYY') }}</div>
            </template>

            <template v-else-if="column.key === 'action'">
                <Button type="text" :icon="h(CloseOutlined)" @click="deleteTeamPermission(record.id)"
                    :disabled="!props.hasEditPermission">Remove</Button>
            </template>
        </template>
    </Table>

    <Modal v-model:open="openTeamAddModal" title="Add team" destroyOnClose>
        <template #footer>
            <Button @click="openTeamAddModal = false">Cancel</Button>
        </template>
        <AddTeamModal :workspaceId="props.workspaceId" :teams="teams" :boardId="props.boardId"
            @teamAdded="addPermissions" />
    </Modal>
</template>