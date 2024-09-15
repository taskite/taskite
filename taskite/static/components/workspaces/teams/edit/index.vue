<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue';
import { Avatar, Table, Button, Modal, message } from 'ant-design-vue';
import { computed, h, onMounted, ref } from 'vue';
import { workspaceTeamMembershipsAPI, workspaceTeamMembershipsDeleteAPI } from '@/utils/api';
import { generateAvatar } from '@/utils/helpers';
import dayjs from 'dayjs';
import { BackwardOutlined, CloseOutlined, EditOutlined, PlusOutlined } from '@ant-design/icons-vue';

import AddMemberModal from './add-member-modal.vue';

const props = defineProps(['workspace', 'team', 'currentUser'])

const memberships = ref([])
const loadTeamMemberships = async () => {
    try {
        const { data } = await workspaceTeamMembershipsAPI(props.workspace.id, props.team.id)
        memberships.value = data.map(t => {
            return {
                key: t.id,
                ...t
            }
        })
    } catch (error) {
        console.log(error)
    }
}

const members = computed(() => {
    return memberships.value.map(membership => membership.user)
})

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
        title: 'Added',
        key: 'added'
    },
    {
        title: 'Actions',
        key: 'actions'
    }
]

const redirectToTeamsPage = () => {
    window.location.href = `/${props.workspace.slug}/teams/`
}

const openMemberModal = ref(false)
const showMemberModal = () => {
    openMemberModal.value = true
}

const addMembership = (membership) => {
    memberships.value.push(membership)
}

const removeMembership = async (membership) => {
    try {
        await workspaceTeamMembershipsDeleteAPI(props.workspace.id, membership.id)
        message.success(`${membership.user.firstName} ${membership.user?.lastName} has been removed from the team.`)
        memberships.value = memberships.value.filter(m => m.id !== membership.id)
    } catch (error) {
        console.log(error)
    }
}

onMounted(() => {
    loadTeamMemberships()
})
</script>

<template>
    <WorkspaceLayout :workspace="props.workspace" :currentUser="props.currentUser" page="teams">
        <div class="mb-3 text-primary" @click="redirectToTeamsPage">
            <BackwardOutlined />
            <span class="hover:underline hover:underline-offset-4 hover:cursor-pointer ml-1">Back to teams</span>
        </div>
        <div class="flex justify-between">
            <div class="text-2xl mb-3 flex gap-2 items-center">
                <div>
                    {{ props.team.name }}
                </div>
            </div>
            <div>
                <Button :icon="h(PlusOutlined)" type="primary" @click="showMemberModal">Add member</Button>
            </div>
        </div>
        <div>
            <Table :dataSource="memberships" :columns="columns">
                <template #bodyCell="{ column, record }">
                    <template v-if="column.key === 'name'">
                        <div class="flex items-center gap-2">
                            <Avatar :src="generateAvatar(record.user.firstName)" />
                            <div class="flex flex-col">
                                <div>{{ record.user.firstName }} {{ record.user?.lastName }}</div>
                                <div class="text-xs text-gray-600">@{{ record.user.username }}</div>
                            </div>
                        </div>
                    </template>

                    <template v-else-if="column.key === 'email'">
                        <div>{{ record.user.email }}</div>
                    </template>

                    <template v-else-if="column.key === 'added'">
                        <div>{{ dayjs(record.createdAt).format('D MMM YY') }}</div>
                    </template>

                    <template v-else-if="column.key === 'actions'">
                        <div class="flex gap-2">
                            <Button type="text" :icon="h(CloseOutlined)"
                                @click="removeMembership(record)">Remove</Button>
                        </div>
                    </template>
                </template>
            </Table>
        </div>
    </WorkspaceLayout>

    <Modal v-model:open="openMemberModal" title="Add member">
        <template #footer>
            <Button @click="openMemberModal = false">Cancel</Button>
        </template>
        <AddMemberModal :workspace="props.workspace" :team="team" :members="members" @membershipAdded="addMembership" />
    </Modal>
</template>