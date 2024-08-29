<script setup>
import BoardPriorityFilters from '@/components/boards/BoardPriorityFilters.vue'
import BoardAssigneeFilters from '@/components/boards/BoardAssigneeFilters.vue'
import { useBoardStore } from '@/stores/board'
import {
  boardDetailAPI,
  boardMembersAPI,
  priorityListAPI,
  stateListAPI,
  taskListAPI,
} from '@/utils/api'
import { generateAvatar } from '@/utils/generators'
import {
  CloseOutlined,
  FilterOutlined,
  PlusOutlined,
} from '@ant-design/icons-vue'
import { onMounted, ref, onBeforeMount, h } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'
import { useRoute } from 'vue-router'

const route = useRoute()
const boardStore = useBoardStore()
const groupBy = ref('none')

const loading = ref(false)

const fetchStates = async (boardId) => {
  try {
    const { data } = await stateListAPI(boardId)
    return data
  } catch (error) {
    console.log(error)
    return []
  }
}

const fetchPriorities = async (boardId) => {
  try {
    const { data } = await priorityListAPI(boardId)
    return data
  } catch (error) {
    console.log(error)
  }
}

const fetchTasks = async (boardId) => {
  try {
    const { data } = await taskListAPI(boardId)
    return data
  } catch (error) {
    console.log(error)
    return []
  }
}

const loadBoardMembers = async () => {
  try {
    const { data } = await boardMembersAPI(route.params.boardId)
    boardStore.setMembers(data)
  } catch (error) {
    console.log(error)
    return []
  }
}

const loadBoardItems = async () => {
  const boardId = route.params.boardId

  // Fetch State
  const states = await fetchStates(boardId)
  boardStore.setStates(states)

  // Fetch Priorities
  const priorities = await fetchPriorities(boardId)
  boardStore.setPriorities(priorities)

  // Fetch tasks kanban
  const tasks = await fetchTasks(boardId)
  boardStore.setTasks(tasks)
}

onMounted(async () => {
  loading.value = true

  await loadBoardMembers()
  await loadBoardItems()
  await boardStore.loadKanban()

  loading.value = false
})

const showFilterDropdown = ref(false)
</script>

<template>
  <div v-if="loading" class="flex justify-center items-center h-screen">
    <a-skeleton active class="px-3" :paragraph="{ rows: 20 }"></a-skeleton>
  </div>
  <div class="h-screen flex flex-col" v-else>
    <div
      class="flex flex-row justify-between items-center pb-3 px-3 task-header"
    >
      <div class="flex gap-1">
        <a-avatar-group :max-count="5">
          <a-tooltip
            :title="member.firstName"
            placement="top"
            v-for="member in boardStore.members"
            :key="member.id"
          >
            <a-avatar :src="generateAvatar(member.firstName)"></a-avatar>
          </a-tooltip>
        </a-avatar-group>
      </div>

      <div class="flex flex-row gap-1 items-center">
        <a-dropdown
          :trigger="['click']"
          placement="bottomRight"
          v-model:open="showFilterDropdown"
        >
          <a-button type="text" :icon="h(FilterOutlined)">Filters</a-button>
          <template #overlay>
            <a-card size="small" title="Filters" class="w-80">
              <template #extra>
                <a-button
                  :icon="h(CloseOutlined)"
                  size="small"
                  @click="showFilterDropdown = false"
                ></a-button>
              </template>
              <BoardPriorityFilters />
              <a-divider style="margin: 12px 0;" />
              <BoardAssigneeFilters />
            </a-card>
          </template>
        </a-dropdown>
        <a-divider
          type="vertical"
          style="height: 20px; background-color: darkgray"
        />
        <a-dropdown :trigger="['click']" placement="bottomRight">
          <a-button type="dashed" class="text-xs">GROUP BY</a-button>
          <template #overlay>
            <a-card size="small" class="w-48">
              <a-radio-group v-model:value="groupBy" class="flex flex-col">
                <a-radio value="none">None</a-radio>
                <a-radio value="priorities">Priorities</a-radio>
                <a-radio value="members">Members</a-radio>
              </a-radio-group>
            </a-card>
          </template>
        </a-dropdown>
        <a-divider
          type="vertical"
          style="height: 20px; background-color: darkgray"
        />
        <a-button type="primary" :icon="h(PlusOutlined)">New task</a-button>
      </div>
    </div>
    <div class="flex gap-2 overflow-x-auto h-full px-3">
      <div
        class="w-80 flex-shrink-0"
        v-for="state in boardStore.kanban"
        :key="state.id"
      >
        <div class="font-semi-bold text-lg my-1">{{ state.name }}</div>
        <VueDraggable
          class="flex flex-col gap-2 overflow-y-auto state-tasks"
          v-model="state.tasks"
          style=""
          group="states"
        >
          <a-card
            class="w-full"
            size="small"
            v-for="task in state.tasks"
            :key="task.id"
          >
            <div class="flex justify-between">
              <div class="font-light text-xs">{{ task.name }}</div>
              <div class="text-xs">{{ task.priority.name }}</div>
            </div>
            <div>{{ task.summary }}</div>
            <div class="mt-2">
              <a-avatar-group>
                <a-avatar
                  size="small"
                  v-for="assignee in task.assignees"
                  :key="assignee.id"
                  :src="generateAvatar(assignee.firstName)"
                ></a-avatar>
              </a-avatar-group>
            </div>
          </a-card>
        </VueDraggable>
        <a-button type="link" :icon="h(PlusOutlined)">Add a task</a-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.task-header {
  border-bottom: 2px solid darkgray;
}

.state-tasks {
  max-height: calc(100% - 9rem);
}

/* Custom scrollbar for the draggable container */
.state-tasks::-webkit-scrollbar {
  width: thin; /* Width of the scrollbar */
}

.state-tasks::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.5); /* Scrollbar color */
  border-radius: 4px; /* Rounded corners */
}

.state-tasks::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.1); /* Background track color */
}
</style>
