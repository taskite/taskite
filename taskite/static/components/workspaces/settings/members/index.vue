<script setup>
import { computed, h, onMounted, ref } from 'vue';
import { Button, message, Modal, TabPane, Tabs } from 'ant-design-vue'

import WorkspaceSettingsLayout from '@/components/base/workspace-settings-layout.vue';
import ActiveMembers from '@/components/workspaces/settings/members/active-members.vue';
import PendingInvites from '@/components/workspaces/settings/members/pending-invites.vue'
import { workspaceMembershipsAPI, workspaceInvitesAPI, workspaceMembershipsDeleteAPI, workspaceInvitesDeleteAPI } from '@/utils/api';
import { PlusOutlined } from '@ant-design/icons-vue';
import InviteMemberModal from '@/components/workspaces/settings/members/invite-member-modal.vue';
import { handleResponseError } from '@/utils/helpers';

const activeTab = ref('active_members')

const props = defineProps(['workspace', 'membershipRole', 'pageTitle', 'currentUser'])

const memberships = ref([])
const fetchMemberships = async () => {
    try {
        const { data } = await workspaceMembershipsAPI(props.workspace.id)
        memberships.value = data.map(membership => {
            return {
                key: membership.id,
                ...membership
            }
        })
    } catch (error) {
        handleResponseError(error)
    }
}

const invites = ref([])
const loadWorkspaceInvites = async () => {
    try {
        const { data } = await workspaceInvitesAPI(props.workspace.id)
        invites.value = data.map((i) => {
            return {
                key: i.id,
                ...i
            }
        })
    } catch (error) {
        handleResponseError(error)
    }
}

const notAdmin = computed(() => {
    return props.membershipRole !== 'admin'
})

const openInviteMemberModal = ref(false)
const showOpenInviteMemberModal = () => {
    openInviteMemberModal.value = true
}

const addInvites = (newInvites) => {
    invites.value = [...invites.value, ...newInvites]

    // Show message
    message.success('Invites has been sent to the emails to join the workspace!')

    // Close the modal
    openInviteMemberModal.value = false
}

const removeMembership = async (membershipId) => {
    try {
        await workspaceMembershipsDeleteAPI(props.workspace.id, membershipId)
        memberships.value = memberships.value.filter(membership => membership.id !== membershipId)

        message.success('Membership got removed!')
    } catch (error) {
        handleResponseError(error)
    }
}

const removeInvite = async (inviteId) => {
    try {
        await workspaceInvitesDeleteAPI(props.workspace.id, inviteId)
        invites.value = invites.value.filter(invite => invite.id !== inviteId)

        message.success('Invite got removed!')
    } catch (error) {
        handleResponseError(error)
    }
}

onMounted(() => {
    fetchMemberships()
    loadWorkspaceInvites()
})
</script>

<template>
    <WorkspaceSettingsLayout :workspace="props.workspace" page="members" :currentUser="props.currentUser">
        <Tabs type="card" v-model:activeKey="activeTab">
            <TabPane tab="Active members" key="active_members">
                <ActiveMembers :memberships="memberships" :notAdmin="notAdmin" :workspaceId="props.workspace.id"
                    @remove="removeMembership" />
            </TabPane>
            <TabPane tab="Pending invites" key="pending_invites">
                <PendingInvites :workspaceId="props.workspace.id" :invites="invites" :notAdmin="notAdmin"
                    @remove="removeInvite">
                </PendingInvites>
            </TabPane>

            <template #rightExtra>
                <Button type="primary" :icon="h(PlusOutlined)" class="mb-1" :notAdmin="notAdmin"
                    @click="showOpenInviteMemberModal">Invite members</Button>
            </template>
        </Tabs>
    </WorkspaceSettingsLayout>

    <Modal v-model:open="openInviteMemberModal" title="Invite members">
        <InviteMemberModal :workspaceId="props.workspace.id" @invited="addInvites" />

        <template #footer>
            <Button @click="openInviteMemberModal = false">Cancel</Button>
        </template>
    </Modal>
</template>

<style scoped></style>