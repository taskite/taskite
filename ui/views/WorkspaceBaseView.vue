<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import {
  AppleOutlined,
  AndroidOutlined,
  GatewayOutlined,
  GlobalOutlined,
  TeamOutlined,
  UngroupOutlined,
  NotificationOutlined,
  MoneyCollectOutlined,
  CreditCardOutlined,
  ControlOutlined,
  UserOutlined,
} from '@ant-design/icons-vue'

import { onMounted, ref, watch } from 'vue'
import { workspaceDetailAPI } from '@/utils/api'

const route = useRoute()
const router = useRouter()

const activeKey = ref(route.name)

const workspace = ref(null)

const loadWorkspace = async () => {
  try {
    const { data } = await workspaceDetailAPI(route.params.workspaceId)
    workspace.value = data
  } catch (error) {
    console.log(error)
  }
}

const changeTab = (key) => {
  router.push({ name: key, params: { workspaceId: workspace.id } })
}

onMounted(async () => {
  await loadWorkspace()
})

watch(
  () => route.params.workspaceId,
  async () => {
    await loadWorkspace()
  }
)
</script>

<template>
  <div v-if="!!workspace">
    <a-typography-title :level="3">{{ workspace.name }}</a-typography-title>
    <a-tabs v-model:activeKey="activeKey" @change="changeTab">
      <a-tab-pane key="workspace-general">
        <template #tab>
          <span>
            <GlobalOutlined />
            General
          </span>
        </template>
      </a-tab-pane>
      <a-tab-pane key="workspace-members">
        <template #tab>
          <span>
            <UserOutlined />
            Members
          </span>
        </template>
      </a-tab-pane>

      <a-tab-pane key="workspace-teams">
        <template #tab>
          <span>
            <TeamOutlined />
            Teams
          </span>
        </template>
      </a-tab-pane>

      <a-tab-pane key="workspace-notifications">
        <template #tab>
          <span>
            <NotificationOutlined />
            Notifications
          </span>
        </template>
      </a-tab-pane>

      <a-tab-pane key="workspace-billing">
        <template #tab>
          <span>
            <CreditCardOutlined />
            Billing
          </span>
        </template>
      </a-tab-pane>

      <a-tab-pane key="workspace-advance">
        <template #tab>
          <span>
            <ControlOutlined />
            Advance
          </span>
        </template>
      </a-tab-pane>
    </a-tabs>
    <RouterView :workspace="workspace" />
  </div>
</template>
