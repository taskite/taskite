<script setup>
import { boardMembershipListAPI } from '@/utils/api'
import { computed, h, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import {
  CloseOutlined,
  UserAddOutlined,
  UsergroupAddOutlined,
} from '@ant-design/icons-vue'
import CollaboratorAddUserModal from '@/components/boards/settings/CollaboratorAddUserModal.vue'
import CollaboratorAddTeamModal from '@/components/boards/settings/CollaboratorAddTeamModal.vue'

dayjs.extend(relativeTime)

const route = useRoute()

const memberships = ref([])
const selectedRowKeys = ref([])
const loadMemberships = async () => {
  try {
    const { data } = await boardMembershipListAPI(route.params.boardId)
    memberships.value = data
  } catch (error) {
    console.log(error)
  }
}
const membershipsDataSource = computed(() => {
  return memberships.value.map((m) => {
    return {
      key: m.id,
      ...m,
    }
  })
})
const onSelectChange = (keys) => {
  //   console.log('selectedRowKeys changed: ', keys)
  selectedRowKeys.value = keys
}

const columns = [
  {
    title: 'Users/Teams',
    key: 'users_teams',
  },
  {
    title: 'Role',
    key: 'role',
  },
  {
    title: 'Added',
    key: 'added',
  },
  {
    title: 'Action',
    key: 'action',
  },
]

const openAddUserModal = ref(false)
const showAddUserModal = () => {
  openAddUserModal.value = true
}

onMounted(() => {
  loadMemberships()
})
</script>

<template>
  <a-table
    :dataSource="membershipsDataSource"
    :columns="columns"
    :showHeader="false"
    :rowSelection="{
      selectedRowKeys: selectedRowKeys,
      onChange: onSelectChange,
    }"
  >
    <template #bodyCell="{ column, record }">
      <template v-if="column.key === 'users_teams'">
        <a v-if="record.user"
          >{{ record.user.firstName }} {{ record.user?.lastName }}</a
        >
        <a v-else>{{ record.team.name }}</a>
      </template>

      <template v-if="column.key === 'role'">
        <a-select :value="record.role" style="width: 150px">
          <a-select-option value="admin">Admin</a-select-option>
          <a-select-option value="collaborator">Collaborator</a-select-option>
        </a-select>
      </template>

      <template v-if="column.key === 'added'">
        {{ dayjs(record.createdAt).fromNow() }}
      </template>

      <template v-if="column.key === 'action'">
        <a class="text-slate-500">
          <CloseOutlined />
          <span class="ml-1">Remove</span>
        </a>
      </template>
    </template>

    <template #title>
      <div class="flex justify-between items-center">
        <div class="text-2xl font-bold">Collaborators</div>
        <div class="flex gap-3">
          <a-button
            type="primary"
            :icon="h(UserAddOutlined)"
            @click="showAddUserModal"
            >Add user</a-button
          >
          <a-button type="primary" :icon="h(UsergroupAddOutlined)"
            >Add team</a-button
          >
        </div>
      </div>
    </template>
  </a-table>

  <a-modal v-model:open="openAddUserModal" title="Add user to the board">
    <CollaboratorAddUserModal />
  </a-modal>
</template>
