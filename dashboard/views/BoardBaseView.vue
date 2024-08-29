<script setup>
import {
  TeamOutlined,
  ProjectOutlined,
  TableOutlined,
  SettingOutlined,
  ClockCircleOutlined,
  CalendarOutlined,
  CarryOutOutlined,
  LeftOutlined,
} from '@ant-design/icons-vue'
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { h, onMounted, ref } from 'vue'
import { useBoardStore } from '@/stores/board'
import { boardDetailAPI } from '@/utils/api'

const activeKey = ref('board')
const boardStore = useBoardStore()

const route = useRoute()

const fetchBoard = async () => {
  try {
    const { data } = await boardDetailAPI(route.params.boardId)
    boardStore.setSelectedBoard(data)
  } catch (error) {
    console.log(error)
  }
}

onMounted(async () => {
  await fetchBoard()
})
</script>

<template>
  <div class="ml-2">
    <a-tabs v-model:activeKey="activeKey">
      <a-tab-pane key="board">
        <template #tab>
          <span>
            <ProjectOutlined />
            Board
          </span>
        </template>
      </a-tab-pane>
      <a-tab-pane key="table">
        <template #tab>
          <span>
            <TableOutlined />
            Table
          </span>
        </template>
      </a-tab-pane>

      <a-tab-pane key="timeline">
        <template #tab>
          <span>
            <ClockCircleOutlined />
            Timeline
          </span>
        </template>
      </a-tab-pane>

      <a-tab-pane key="calender">
        <template #tab>
          <span>
            <CalendarOutlined />
            Calender
          </span>
        </template>
      </a-tab-pane>

      <a-tab-pane key="sprints">
        <template #tab>
          <span>
            <CarryOutOutlined />
            Sprints
          </span>
        </template>
      </a-tab-pane>

      <a-tab-pane key="members">
        <template #tab>
          <span>
            <TeamOutlined />
            Members
          </span>
        </template>
      </a-tab-pane>

      <a-tab-pane key="settings">
        <template #tab>
          <span>
            <SettingOutlined />
            Settings
          </span>
        </template>
      </a-tab-pane>

      <template #leftExtra>
        <a-button class="mr-4" type="text">
          <a-typography-title :level="5">{{
            boardStore.selectedBoard?.name
          }}</a-typography-title>
        </a-button>
      </template>

      <template #rightExtra>
        <RouterLink :to="{ name: 'home-base' }">
          <a-button :icon="h(LeftOutlined)" class="mr-2" type="text">
            Back to Home
          </a-button>
        </RouterLink>
      </template>
    </a-tabs>
  </div>

  <RouterView />
</template>

<style scoped></style>
