<script setup>
import WorkspaceSettingsLayout from '@/components/base/workspace-settings-layout.vue';
import { message, Table, Avatar, AvatarGroup, Button, Modal, Dropdown, Menu, MenuItem } from 'ant-design-vue';
import { computed, h, onMounted, ref } from 'vue';
import { generateAvatar } from '@/utils/helpers';
import { CloseOutlined, DownOutlined, EditOutlined, PlusOutlined } from '@ant-design/icons-vue';
import dayjs from 'dayjs';
import TeamAddModal from './team-add-modal.vue';
import { workspaceTeamDeleteAPI, workspaceTeamsAPI } from '@/utils/api';
import { handleResponseError } from '@/utils/helpers';


const props = defineProps(['workspace', 'currentUser', 'membershipRole'])

console.log(props)

const teams = ref([])
const error = ref('')
const fetchTeams = async () => {
    try {
        const { data } = await workspaceTeamsAPI(props.workspace.id)
        teams.value = data.map(team => {
            return {
                key: team.id,
                ...team
            }
        })
    } catch (err) {
        handleResponseError(err)
    }
}

const columns = [
    {
        title: 'Name',
        key: 'name'
    },
    {
        title: 'Members',
        key: 'members'
    },
    {
        title: 'Created',
        key: 'created'
    },
    {
        title: 'Actions',
        key: 'actions'
    }
]

const redirectToEditPage = (team) => {
    window.location.href = `/${props.workspace.slug}/settings/teams/${team.id}/edit`
}

const openTeamAddModal = ref(false)
const showTeamAddModal = () => [
    openTeamAddModal.value = true
]
const addTeam = (team) => {
    teams.value.push(team)
    openTeamAddModal.value = false
}

const removeTeam = async (team) => {
    try {
        await workspaceTeamDeleteAPI(props.workspace.id, team.id)
        teams.value = teams.value.filter(t => t.id !== team.id)
    } catch (error) {
        handleResponseError(error)
    }
}

const notAdmin = computed(() => {
    return props.membershipRole !== 'admin'
})

onMounted(() => {
    fetchTeams()
})
</script>

<template>
    <WorkspaceSettingsLayout :workspace="props.workspace" page="teams" :currentUser="props.currentUser">
        <div class="flex justify-between mb-4">
            <div class="text-2xl">Teams</div>

            <div>
                <Button :icon="h(PlusOutlined)" type="primary" @click="showTeamAddModal" :disabled="notAdmin">Create
                    team</Button>
            </div>
        </div>
        <Table :dataSource="teams" :columns="columns">
            <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'name'">
                    <div class="flex gap-2 items-center">
                        <Avatar :src="record.avatar ? record.avatar : generateAvatar(record.name)" />
                        <div>{{ record.name }}</div>
                    </div>
                </template>

                <template v-else-if="column.key === 'members'">
                    <Dropdown :trigger="['click']">
                        <div class="flex gap-2">
                            <AvatarGroup :maxCount="5" size="small">
                                <Avatar v-for="member in record.members" :key="member.id"
                                    :src="generateAvatar(member.firstName)" size="small" />
                            </AvatarGroup>

                            <DownOutlined v-if="record.members.length > 0" />
                        </div>
                        <template #overlay>
                            <Menu>
                                <MenuItem v-for="member in record.members" :key="member.id">
                                <div class="flex gap-3 items-center">
                                    <Avatar :src="generateAvatar(member.firstName, 20)" />

                                    <div class="flex flex-col">
                                        <div>{{ member.firstName }} {{ member?.lastName }}</div>
                                        <div>{{ member.email }}</div>
                                    </div>
                                </div>
                                </MenuItem>
                            </Menu>
                        </template>
                    </Dropdown>
                </template>

                <template v-else-if="column.key === 'created'">
                    {{ dayjs(record.createdAt).format('D MMM YY') }}
                </template>

                <template v-else-if="column.key === 'actions'">
                    <div class="flex gap-2">
                        <Button :icon="h(EditOutlined)" type="text" @click="redirectToEditPage(record)"
                            :disabled="notAdmin">Edit</Button>
                        <Button :icon="h(CloseOutlined)" type="text" class="text-gray-500" @click="removeTeam(record)"
                            :disabled="notAdmin">Remove</Button>
                    </div>
                </template>
            </template>
        </Table>
    </WorkspaceSettingsLayout>

    <Modal v-model:open="openTeamAddModal" title="Create team">
        <template #footer>
            <Button @click="openTeamAddModal = false">Cancel</Button>
        </template>
        <TeamAddModal :workspace="props.workspace" @teamAdded="addTeam" />
    </Modal>
</template>