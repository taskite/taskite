<script setup>
import { h, onMounted, ref } from 'vue';
import { Button, message, Modal, TabPane, Tabs } from 'ant-design-vue'

import WorkspaceSettingsLayout from '@/components/base/workspace-settings-layout.vue';
import ActiveMembers from '@/components/workspaces/settings/members/active-members.vue';
import PendingInvites from '@/components/workspaces/settings/members/pending-invites.vue'
import { workspaceMembershipsAPI, workspaceInvitesAPI, workspaceMembershipsDeleteAPI, workspaceInvitesDeleteAPI } from '@/utils/api';
import { CheckCircleOutlined, ClockCircleOutlined, UsergroupAddOutlined } from '@ant-design/icons-vue';
import InviteMemberModal from '@/components/workspaces/settings/members/invite-member-modal.vue';
import { handleResponseError } from '@/utils/helpers';

const activeTab = ref('active_members')

const props = defineProps(['workspace', 'hasEditPermission'])

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
    <WorkspaceSettingsLayout :workspace="props.workspace" page="members">
        <Tabs type="card" v-model:activeKey="activeTab">
            <TabPane key="active_members">
                <template #tab>
                    <span>
                        <CheckCircleOutlined />
                        Active members
                    </span>
                </template>
                <ActiveMembers :memberships="memberships" :workspaceId="props.workspace.id"
                    :hasEditPermission="props.hasEditPermission" @remove="removeMembership" />
            </TabPane>
            <TabPane key="pending_invites">
                <template #tab>
                    <span>
                        <ClockCircleOutlined />
                        Pending invites
                    </span>
                </template>
                <PendingInvites :workspaceId="props.workspace.id" :invites="invites"
                    :hasEditPermission="props.hasEditPermission" @remove="removeInvite">
                </PendingInvites>
            </TabPane>

            <template #rightExtra>
                <Button type="primary" :icon="h(UsergroupAddOutlined)" class="mb-4" :disabled="!props.hasEditPermission"
                    @click="showOpenInviteMemberModal">Invite members</Button>
            </template>
        </Tabs>

        <Modal v-model:open="openInviteMemberModal" title="Invite members">
            <InviteMemberModal :workspaceId="props.workspace.id" @invited="addInvites" />

            <template #footer>
                <Button @click="openInviteMemberModal = false">Cancel</Button>
            </template>
        </Modal>
    </WorkspaceSettingsLayout>
</template>

<style scoped></style>