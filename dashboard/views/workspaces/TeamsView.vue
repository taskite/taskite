<script setup>
import { teamListAPI } from '@/utils/api'
import { generateAvatar } from '@/utils/generators'
import {
  CaretDownOutlined,
  DeleteOutlined,
  DownOutlined,
  EditOutlined,
  PlusOutlined,
} from '@ant-design/icons-vue'
import { computed, h, onMounted, ref } from 'vue'

const props = defineProps(['workspace'])
const teams = ref([])

const teamDataSource = computed(() => {
  return teams.value.map((team) => {
    return {
      ...team,
      key: team.id,
    }
  })
})

const teamColumns = [
  {
    title: 'Name',
    // dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'Members',
    // dataIndex: 'members',
    key: 'members',
  },
  {
    title: 'Action',
    key: 'action',
  },
]

const loadTeams = async () => {
  try {
    const { data } = await teamListAPI(props.workspace.id)
    teams.value = data
  } catch (error) {
    console.log(error)
  }
}

onMounted(() => {
  loadTeams()
})
</script>

<template>
  <div class="flex justify-between mb-4">
    <div></div>

    <div>
      <a-button :icon="h(PlusOutlined)" type="primary">Add team</a-button>
    </div>
  </div>
  <a-table :dataSource="teamDataSource" :columns="teamColumns">
    <template #bodyCell="{ column, record }">
      <template v-if="column.key === 'name'">
        <div>{{ record.name }}</div>
      </template>

      <template v-else-if="column.key === 'members'">
        <div>
          <a-dropdown :trigger="['click']">
            <div class="flex items-center">
              <a-avatar-group :maxCount="5" size="small">
                <a-avatar
                  v-for="member in record.members"
                  size="small"
                  :src="generateAvatar(member.firstName)"
                />
              </a-avatar-group>
              <div>
                <DownOutlined />
              </div>
            </div>

            <template #overlay>
              <a-menu>
                <a-menu-item
                  :key="member.id"
                  v-for="member in record.members"
                  :id="member.id"
                >
                  <div>
                    <a-avatar
                      class="mr-2"
                      :src="generateAvatar(member.firstName)"
                      size="small"
                    ></a-avatar>
                    <span> {{ member.firstName }} {{ member?.lastName }} </span>
                  </div>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </template>

      <template v-else-if="column.key === 'action'">
        <a-button type="link" :icon="h(EditOutlined)">Edit</a-button>
        <a-divider type="vertical" />
        <a-button type="link" :icon="h(DeleteOutlined)">Delete</a-button>
      </template>
    </template>
  </a-table>
</template>
