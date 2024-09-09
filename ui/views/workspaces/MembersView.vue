<script setup>
import {
  workspaceInviteDeleteAPI,
  workspaceInviteListAPI,
  workspaceMembershipDeleteAPI,
  workspaceMembershipListAPI,
} from '@/utils/api'
import { generateAvatar } from '@/utils/generators'
import {
  CaretDownOutlined,
  CloseOutlined,
  DeleteOutlined,
  PlusOutlined,
} from '@ant-design/icons-vue'
import MemberInvite from '@/components/workspaces/MemberInvite.vue'

import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

import { onMounted, ref, h, computed } from 'vue'
import Spinner from '@/components/base/Spinner.vue'
import { message } from 'ant-design-vue'

const props = defineProps(['workspace'])

const invites = ref([])
const loadPendingInvites = async () => {
  try {
    const { data } = await workspaceInviteListAPI(props.workspace.id)
    invites.value = data
  } catch (error) {
    console.log(error)
  }
}

const membersLoading = ref(false)
const memberships = ref([])
const loadMemberships = async () => {
  try {
    membersLoading.value = true
    const { data } = await workspaceMembershipListAPI(props.workspace.id)
    memberships.value = data
  } catch (error) {
    console.log(error)
  } finally {
    membersLoading.value = false
  }
}
const deleteWorkspaceMembership = async (membership) => {
  try {
    console.log(membership)
    await workspaceMembershipDeleteAPI(props.workspace.id, membership.id)
    memberships.value = memberships.value.filter((m) => m.id !== membership.id)
  } catch (error) {
    console.log(error)
  }
}

const membershipsDataSource = computed(() => {
  return memberships.value.map((membership) => {
    return {
      ...membership,
      key: membership.id,
    }
  })
})

const membershipColumns = [
  {
    title: 'Name',
    key: 'name',
  },
  {
    title: 'Username',
    key: 'username',
  },
  {
    title: 'Role',
    key: 'role',
  },
  {
    title: 'Teams',
    key: 'teams',
  },
  {
    title: 'Joined',
    key: 'joined',
  },
  {
    title: 'Action',
    key: 'action',
  },
]

const searchVal = ref('')
const onMemberSearch = (searchValue) => {
  console.log(searchValue)
}

const memberInviteModalOpen = ref(false)
const openMemberInviteModal = () => {
  memberInviteModalOpen.value = true
}
const updateInvites = (invitesData) => {
  invites.value.push(...invitesData)
  memberInviteModalOpen.value = false
}
const deleteInvitation = async (invite) => {
  try {
    await workspaceInviteDeleteAPI(props.workspace.id, invite.id)
    invites.value = invites.value.filter((i) => i.id !== invite.id)
  } catch (error) {
    console.log(error)
  }
}

onMounted(() => {
  loadMemberships()
  loadPendingInvites()
})
</script>

<template>
  <div class="flex items-center justify-between mb-4">
    <div>
      <a-input-search
        v-model:value="searchVal"
        placeholder="Search members"
        style="width: 300px"
        @search="onMemberSearch"
      />
    </div>

    <div class="flex gap-4">
      <a-dropdown :trigger="['click']">
        <a-badge :count="invites.length">
          <a-button> View pending invitations </a-button>
        </a-badge>

        <template #overlay>
          <a-card size="small" class="w-90">
            <div
              class="flex justify-between items-center"
              v-for="invite in invites"
              :key="invite.id"
            >
              <div>
                {{ invite.email }}
              </div>

              <div>
                <a-button
                  type="link"
                  :icon="h(DeleteOutlined)"
                  @click="deleteInvitation(invite)"
                  >Remove</a-button
                >
              </div>
            </div>
          </a-card>
        </template>
      </a-dropdown>
      <a-button
        :icon="h(PlusOutlined)"
        type="primary"
        @click="openMemberInviteModal"
        >Invite member</a-button
      >
    </div>
  </div>

  <div class="flex items-center justify-center" v-if="membersLoading">
    <Spinner />
  </div>
  <a-table
    :dataSource="membershipsDataSource"
    :columns="membershipColumns"
    v-else
  >
    <template #bodyCell="{ column, record }">
      <template v-if="column.key === 'name'">
        <div>
          <a-avatar
            class="mr-2"
            :src="generateAvatar(record.user.firstName)"
            size="small"
          ></a-avatar>
          <span> {{ record.user.firstName }} {{ record.user?.lastName }} </span>
        </div>
      </template>

      <template v-else-if="column.key === 'username'">
        <div>
          {{ record.user.username }}
        </div>
      </template>

      <template v-else-if="column.key === 'role'">
        <div>
          <a-select :value="record.role" style="width: 120px">
            <a-select-option value="admin">Admin</a-select-option>
            <a-select-option value="collaborator">Collaborator</a-select-option>
            <a-select-option value="guest">Guest</a-select-option>
          </a-select>
        </div>
      </template>

      <template v-else-if="column.key === 'teams'">
        <div>
          <a-tag
            :bordered="false"
            v-for="team in record.user.teams"
            :key="team.id"
            >{{ team.name }}</a-tag
          >
        </div>
      </template>

      <template v-else-if="column.key === 'joined'">
        <div>
          {{ dayjs(record.createdAt).fromNow() }}
        </div>
      </template>

      <template v-else-if="column.key === 'action'">
        <div>
          <a class="text-slate-500" @click="deleteWorkspaceMembership(record)">
            <CloseOutlined />
            <span> Remove </span>
          </a>
        </div>
      </template>
    </template>
  </a-table>

  <a-modal
    v-model:open="memberInviteModalOpen"
    title="Member Invite"
    :footer="null"
  >
    <MemberInvite :workspaceId="props.workspace.id" @invited="updateInvites" />
  </a-modal>
</template>
