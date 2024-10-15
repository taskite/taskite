<script setup>
import { computed, h, onMounted, ref } from 'vue';
import { Avatar, Select, SelectOption, Table, Button, Modal, message } from 'ant-design-vue';
import { generateAvatar, handleResponseError } from '@/utils/helpers';
import dayjs from 'dayjs';
import { CloseOutlined, UserAddOutlined } from '@ant-design/icons-vue';
import AddUserModal from './add-user-modal.vue';
import { boardPermissionUpdateAPI, boardPermissionListAPI, boardPermissionDeleteAPI } from '@/utils/api';

const props = defineProps(['boardId', 'workspaceId', 'hasEditPermission'])

const permissions = ref([])
const loadBoardPermissions = async () => {
    try {
        const { data } = await boardPermissionListAPI(props.boardId)
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
    loadBoardPermissions()
})

const columns = [
    {
        title: 'User',
        key: 'user'
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
        await boardPermissionUpdateAPI(props.boardId, permissionId, updateData)
        message.success('Board permission updated successfully.')
    } catch (error) {
        handleResponseError(error)
    }
}

const deletePermission = async (permissionId) => {
    try {
        await boardPermissionDeleteAPI(props.boardId, permissionId)
        permissions.value = permissions.value.filter(permission => permission.id !== permissionId)
        message.success('Permission has been removed')
    } catch (error) {
        handleResponseError(error)
    }
}

const openUserAddModal = ref(false)
const showUserAddModal = () => {
    openUserAddModal.value = true
}
const users = computed(() => {
    return permissions.value.map(permission => permission.user)
})
const addPermissions = (data) => {
    permissions.value.push(data)
}
</script>

<template>
    <div class="flex justify-end mb-4">
        <Button :icon="h(UserAddOutlined)" type="primary" @click="showUserAddModal" :disabled="!props.hasEditPermission">Add user</Button>
    </div>
    <Table :columns="columns" :data-source="permissions">
        <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'user'">
                <div class="flex items-center gap-1">
                    <div>
                        <Avatar
                            :src="!!record.user.avatar ? record.user.avatar : generateAvatar(record.user.firstName)" />
                    </div>
                    <div class="flex flex-col">
                        <div>{{ record.user.firstName }} {{ record.user?.lastName }}</div>
                        <div>{{ record.user.email }}</div>
                    </div>
                </div>
            </template>

            <template v-else-if="column.key === 'role'">
                <Select v-model:value="record.role" style="width: 140px"
                    @change="(role) => handleRoleChange(record.id, role)" :disabled="!props.hasEditPermission">
                    <SelectOption value="collaborator">Collaborator</SelectOption>
                    <SelectOption value="admin">Admin</SelectOption>
                </Select>
            </template>

            <template v-else-if="column.key === 'joined'">
                <div>{{ dayjs(record.createdAt).format('MMMM D, YYYY') }}</div>
            </template>

            <template v-else-if="column.key === 'action'">
                <Button type="text" :icon="h(CloseOutlined)" @click="deletePermission(record.id)" :disabled="!props.hasEditPermission">Remove</Button>
            </template>
        </template>
    </Table>

    <Modal v-model:open="openUserAddModal" title="Add user" destroyOnClose>
        <template #footer>
            <Button @click="openUserAddModal = false">Cancel</Button>
        </template>
        <AddUserModal :users="users" :boardId="props.boardId" :workspaceId="props.workspaceId"
            @userAdded="addPermissions" />
    </Modal>
</template>