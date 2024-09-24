<script setup>
import { computed, h, onMounted, ref } from 'vue';
import { Button, Modal, TabPane, Tabs } from 'ant-design-vue'

import WorkspaceSettingsLayout from '@/components/base/workspace-settings-layout.vue';
import ActiveMembers from '@/components/workspaces/settings/members/active-members.vue';
import PendingInvites from '@/components/workspaces/settings/members/pending-invites.vue'
import { workspaceMembershipsAPI } from '@/utils/api/workspaces';
import { PlusOutlined } from '@ant-design/icons-vue';
import InviteMemberModal from '@/components/workspaces/settings/members/invite-member-modal.vue';

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
        console.log(error)
    }
}

const notAdmin = computed(() => {
    return props.membershipRole !== 'admin'
})

const openInviteMemberModal = ref(false)
const showOpenInviteMemberModal = () => {
    openInviteMemberModal.value = true
}

onMounted(() => {
    fetchMemberships()
})
</script>

<template>
    <WorkspaceSettingsLayout :workspace="props.workspace" page="members" :currentUser="props.currentUser">
        <Tabs type="card" v-model:activeKey="activeTab">
            <TabPane tab="Active members" key="active_members">
                <ActiveMembers :memberships="memberships" :notAdmin="notAdmin" :workspaceId="props.workspace.id" />
            </TabPane>
            <TabPane tab="Pending invites" key="pending_invites">
                <PendingInvites :workspaceId="props.workspace.id" :notAdmin="notAdmin"></PendingInvites>
            </TabPane>

            <template #rightExtra>
                <Button type="primary" :icon="h(PlusOutlined)" class="mb-1" :notAdmin="notAdmin"
                    @click="showOpenInviteMemberModal">Invite members</Button>
            </template>
        </Tabs>
    </WorkspaceSettingsLayout>

    <Modal v-model:open="openInviteMemberModal" title="Invite members">
        <InviteMemberModal :workspaceId="props.workspace.id" />

        <template #footer>
            <Button @click="openInviteMemberModal = false">Cancel</Button>
        </template>
    </Modal>
</template>

<style scoped></style>