<script setup>
import BoardSettingsLayout from '@/components/base/board-settings-layout.vue';
import { computed, h, onMounted, ref } from 'vue';
import { boardMembershipsAPI, boardMembershipsDeleteAPI } from '@/utils/api';
import { Avatar, Button, message, Modal, Select, SelectOption, Table, Tag } from 'ant-design-vue';
import { CloseOutlined, TeamOutlined, UserAddOutlined, UsergroupAddOutlined, UserOutlined } from '@ant-design/icons-vue';
import dayjs from 'dayjs';
import { generateAvatar } from '@/utils/helpers';
import AddUserModal from './add-user-modal.vue';
import AddTeamModal from './add-team-modal.vue';
import { boardMembershipsUpdateAPI } from '../../../../../utils/api';

const props = defineProps(['workspace', 'board'])

const memberships = ref([])
const loading = ref(false)

const loadMemberships = async () => {
    try {
        loading.value = true
        const { data } = await boardMembershipsAPI(props.board.id)
        memberships.value = data.map((m) => {
            return {
                key: m.id,
                ...m
            }
        })
    } catch (error) {
        console.log(error)
    } finally {
        loading.value = false
    }
}

const handleRoleChange = async (membershipId, role) => {
    try {
        const updateData = {
            role: role
        }
        await boardMembershipsUpdateAPI(props.board.id, membershipId, updateData)
        message.success('Membership got updated successfully.')
    } catch (error) {
        console.log(error)
    }
}

const columns = [
    {
        title: 'User/Team',
        key: 'user_team'
    },
    {
        title: 'Type',
        key: 'type'
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

const openUserAddModal = ref(false)
const showUserAddModal = () => {
    openUserAddModal.value = true
}

const openTeamAddModal = ref(false)
const showTeamAddModal = () => {
    openTeamAddModal.value = true
}

const users = computed(() => {
    return memberships.value.filter(membership => membership.user).map(membership => membership.user)
})

const teams = computed(() => {
    return memberships.value.filter(membership => membership.team).map(membership => membership.team)
})

const addMembership = (data) => {
    memberships.value.push(data)
}

const deleteMembership = async (membershipId) => {
    try {
        await boardMembershipsDeleteAPI(props.board.id, membershipId)
        memberships.value = memberships.value.filter(membership => membership.id !== membershipId)
    } catch (error) {
        console.log(error)
    }
}

onMounted(() => {
    loadMemberships()
})
</script>

<template>
    <BoardSettingsLayout :workspace="props.workspace" :board="props.board" page="collaborators">
        <div class="flex justify-between items-center mb-3">
            <div class="text-xl">Collaborators</div>

            <div class="flex gap-3">
                <Button type="primary" :icon="h(UserAddOutlined)" @click="showUserAddModal">Add user</Button>
                <Button type="primary" :icon="h(UsergroupAddOutlined)" @click="showTeamAddModal">Add team</Button>
            </div>
        </div>

        <Table :dataSource="memberships" :columns="columns" :loading="loading">
            <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'user_team'">
                    <div v-if="record.team">
                        <div class="flex items-center gap-2">
                            <Avatar :src="generateAvatar(record.team.name, 20)" shape="square" />
                            <div>{{ record.team.name }}</div>
                        </div>
                    </div>

                    <div v-else="record.user">
                        <div class="flex items-center gap-2">
                            <Avatar :src="generateAvatar(record.user.firstName)" />
                            <div class="flex flex-col">
                                <div>{{ record.user.firstName }} {{ record.user?.lastName }}</div>
                                <div class="text-xs">@{{ record.user.username }}</div>
                            </div>
                        </div>
                    </div>
                </template>

                <template v-else-if="column.key === 'type'">
                    <div v-if="record.user">
                        <div>User</div>
                    </div>
                    <div v-else>
                        <div>Team</div>
                    </div>
                </template>

                <template v-else-if="column.key === 'role'">
                    <Select v-model:value="record.role" style="width: 140px"
                        @change="(role) => handleRoleChange(record.id, role)">
                        <SelectOption value="collaborator">Collaborator</SelectOption>
                        <SelectOption value="admin">Admin</SelectOption>
                    </Select>
                </template>

                <template v-else-if="column.key === 'joined'">
                    {{ dayjs(record.createdAt).format('D MMM YY') }}
                </template>

                <template v-else-if="column.key === 'action'">
                    <Button type="text" :icon="h(CloseOutlined)" class="text-gray-500"
                        @click="deleteMembership(record.id)">
                        Remove
                    </Button>
                </template>
            </template>
        </Table>
    </BoardSettingsLayout>

    <Modal v-model:open="openUserAddModal" title="Add user" destroyOnClose>
        <template #footer>
            <Button @click="openUserAddModal = false">Cancel</Button>
        </template>
        <AddUserModal :workspaceId="props.workspace.id" :users="users" :boardId="props.board.id"
            @userAdded="addMembership" />
    </Modal>

    <Modal v-model:open="openTeamAddModal" title="Add team" destroyOnClose>
        <template #footer>
            <Button @click="openTeamAddModal = false">Cancel</Button>
        </template>
        <AddTeamModal :workspaceId="props.workspace.id" :teams="teams" :boardId="props.board.id"
            @teamAdded="addMembership" />
    </Modal>
</template>