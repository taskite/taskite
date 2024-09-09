<script setup>
import { RouterView, useRoute, useRouter } from 'vue-router'
import { ref } from 'vue'
import { ApiOutlined, FlagOutlined, FormOutlined, HistoryOutlined, HolderOutlined, ProjectOutlined, RobotOutlined, SettingOutlined, TagsOutlined, TeamOutlined, ToolOutlined } from '@ant-design/icons-vue'

const route = useRoute()
const router = useRouter()

const selectedKeys = ref([route.name])

const changeTab = (item) => {
  router.push({ name: item.key, params: { boardId: route.params.boardId } })
}
</script>

<template>
  <div class="container mx-auto px-4">
    <a-layout>
      <a-layout-sider
        :style="{
          background: '#fff',
        }"
      >
        <a-menu
          v-model:selectedKeys="selectedKeys"
          mode="inline"
          @select="changeTab"
        >
          <a-menu-item key="board-settings-general">
            <ProjectOutlined />
            <span>General</span>
          </a-menu-item>

          <a-menu-item key="board-settings-collaborators">
            <TeamOutlined />
            <span>Collaborators</span>
          </a-menu-item>

          <a-menu-item key="board-settings-states">
            <FormOutlined />
            <span>States</span>
          </a-menu-item>

          <a-menu-item key="board-settings-priorities">
            <FlagOutlined />
            <span>Priorities</span>
          </a-menu-item>

          <a-menu-item key="board-settings-labels">
            <TagsOutlined />
            <span>Labels</span>
          </a-menu-item>

          <a-menu-item key="board-settings-automations">
            <RobotOutlined />
            <span>Automations</span>
          </a-menu-item>

          <a-menu-item key="board-settings-integrations">
            <ApiOutlined />
            <span>Integrations</span>
          </a-menu-item>

          <a-menu-item key="board-settings-logs">
            <HistoryOutlined />
            <span>Activity Logs</span>
          </a-menu-item>

          <a-menu-item key="board-settings-advance">
            <ToolOutlined />
            <span>Advance</span>
          </a-menu-item>
        </a-menu>
      </a-layout-sider>
      <a-layout>
        <a-layout-content class="px-3 py-2 bg-white">
          <RouterView />
        </a-layout-content>
      </a-layout>
    </a-layout>
  </div>
</template>
