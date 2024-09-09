<script setup>
import { h, onMounted, ref } from 'vue'
import {
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  ProjectOutlined,
  HomeOutlined,
  LogoutOutlined,
  BellOutlined,
  CheckOutlined,
  CloseOutlined,
} from '@ant-design/icons-vue'
import { RouterView } from 'vue-router'
import {
  accountPendingInvitesAPI,
  workspaceListAPI,
  workspaceMembershipsAPI,
} from '@/utils/api'
import { useDashboardStore } from '@/stores/dashboard'
import { generateAvatar } from '@/utils/generators'
import { useUserStore } from '@/stores/user'
import VerificationBanner from '@/components/VerificationBanner.vue'
import PendingInviteList from '@/components/home/PendingInviteList.vue'
import { message } from 'ant-design-vue'
const selectedKeys = ref(['boards'])
const collapsed = ref(false)

const dashboardStore = useDashboardStore()
const userStore = useUserStore()

const fetchWorkspace = async () => {
  try {
    const { data } = await workspaceListAPI()
    return data
  } catch (error) {
    console.log(error)
    return []
  }
}

const pendingInvites = ref([])
const loadPendingInvites = async () => {
  try {
    const { data } = await accountPendingInvitesAPI()
    pendingInvites.value = data
  } catch (error) {
    message.error(error.response.data.detail)
  }
}

const loadWorkspaces = async () => {
  const workspaces = await fetchWorkspace()

  dashboardStore.setWorkspaces(workspaces)
}

onMounted(() => {
  loadWorkspaces()
  loadPendingInvites()
})
</script>

<template>
  <a-layout>
    <a-layout-sider
      v-model:collapsed="collapsed"
      :trigger="null"
      collapsible
      :style="{
        minHeight: '100vh',
        background: '#fff',
        borderRight: '2px solid darkgray',
      }"
    >
      <div class="logo" />
      <a-menu v-model:selectedKeys="selectedKeys" mode="inline">
        <a-menu-item key="boards">
          <RouterLink :to="{ name: 'home-index' }">
            <ProjectOutlined />
            <span>Boards</span>
          </RouterLink>
        </a-menu-item>

        <a-divider></a-divider>

        <a-menu-item-group key="workspaces" title="Workspaces">
          <a-menu-item
            :key="workspace.id"
            v-for="workspace in dashboardStore.workspaces"
          >
            <RouterLink
              :to="{
                name: 'workspace-general',
                params: { workspaceId: workspace.id },
              }"
            >
              <HomeOutlined />
              <span>{{ workspace.name }}</span>
            </RouterLink>
          </a-menu-item>
        </a-menu-item-group>

        <a-divider></a-divider>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <VerificationBanner />
      <a-layout-header
        style="background: #fff; padding: 0; border-bottom: 2px solid darkgray"
      >
        <div class="flex justify-between items-center">
          <div>
            <menu-unfold-outlined
              v-if="collapsed"
              class="trigger"
              @click="() => (collapsed = !collapsed)"
            />
            <menu-fold-outlined
              v-else
              class="trigger"
              @click="() => (collapsed = !collapsed)"
            />
          </div>

          <div>
            <a-dropdown :trigger="['click']">
              <a-button :icon="h(BellOutlined)" type="text" class="mr-2">
                <span>Notifications</span>
                <a-tag
                  class="ml-2"
                  :bordered="false"
                  size="small"
                  color="error"
                  v-if="pendingInvites.length > 0"
                  >{{ pendingInvites.length }}</a-tag
                >
              </a-button>
              <template #overlay>
                <PendingInviteList :invites="pendingInvites" />
              </template>
            </a-dropdown>
            <a-dropdown class="mr-3" :trigger="['click']">
              <a-avatar
                :src="generateAvatar(userStore.loggedInUser.firstName)"
              ></a-avatar>
              <template #overlay>
                <a-card class="w-80" size="small">
                  <div class="flex flex-col gap-1">
                    <div>
                      {{ userStore.loggedInUser.firstName }}
                      {{ userStore.loggedInUser?.lastName }}
                    </div>
                    <div class="text-xs">
                      {{ userStore.loggedInUser.email }}
                    </div>
                    <RouterLink :to="{ name: 'logout' }">
                      <a-button
                        type="dashed"
                        class="mt-2 w-full"
                        :icon="h(LogoutOutlined)"
                        >Logout</a-button
                      >
                    </RouterLink>
                  </div>
                </a-card>
              </template>
            </a-dropdown>
          </div>
        </div>
      </a-layout-header>
      <a-layout-content
        :style="{
          // margin: '24px 16px',
          padding: '24px',
          background: '#fff',
        }"
      >
        <RouterView></RouterView>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<style>
.trigger {
  font-size: 18px;
  line-height: 64px;
  padding: 0 24px;
  cursor: pointer;
  transition: color 0.3s;
}

.trigger:hover {
  color: #1890ff;
}

.logo {
  height: 32px;
  background: rgba(117, 14, 14, 0.3);
  margin: 16px;
}

.site-layout .site-layout-background {
  background: #fff;
}
</style>
