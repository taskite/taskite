<script setup>
import {
  PieChartOutlined,
  DesktopOutlined,
  UserOutlined,
  TeamOutlined,
  FileOutlined,
  ArrowLeftOutlined,
  HomeOutlined,
} from '@ant-design/icons-vue'
import { RouterView, RouterLink } from 'vue-router'
import { h, ref } from 'vue'
const collapsed = ref(false)
const selectedKeys = ref(['tasks'])
</script>

<template>
  <a-layout style="min-height: 100vh">
    <a-layout-sider
      v-model:collapsed="collapsed"
      collapsible
      :style="{  }"
    >
      <div class="p-2">
        <RouterLink :to="{ name: 'home-base' }">
          <a-button type="text" :icon="h(HomeOutlined)" class="w-full">Home</a-button>
        </RouterLink>
      </div>
      <a-menu v-model:selectedKeys="selectedKeys" mode="inline">
        <a-menu-item key="tasks">
          <pie-chart-outlined />
          <span>Tasks</span>
        </a-menu-item>
        <a-menu-item key="members">
          <desktop-outlined />
          <span>Members</span>
        </a-menu-item>
        <a-menu-item key="activity_log">
          <desktop-outlined />
          <span>Activity Log</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <!-- <a-layout-header style="background: #fff; padding: 0" /> -->
      <a-layout-content style="">
        <div
          :style="{ background: '#fff', minHeight: '100vh' }"
        >
          <RouterView></RouterView>
        </div>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<style scoped>
.logo {
  height: 32px;
  margin: 16px;
  background: rgba(152, 22, 22, 0.3);
}

.site-layout .site-layout-background {
  background: #fff;
}

.ant-layout-sider {
    background: #fff;
    border-right: 2px solid darkgray;
}

/* .ant-layout-sider-trigger {
  background-color: #fff;
} */
</style>
