<script setup>
import { useDashboardStore } from '@/stores/dashboard'
import { boardListAPI, boardMembershipsAPI, createBoardAPI } from '@/utils/api'
import { PlusOutlined } from '@ant-design/icons-vue'
import { ref, h, onMounted, watch, onActivated } from 'vue'
import { useRouter } from 'vue-router'
import BoardNew from '@/components/boards/BoardNew.vue'

const router = useRouter()

const searchValue = ref('')
const onBoardSearch = (value) => {
  console.log(value)
}

const dashboardStore = useDashboardStore()

const boardNewModal = ref(false)
const showBoardNewModal = () => {
  boardNewModal.value = true
}
const closeBoardNewModal = () => {
  boardNewModal.value = false
}


const fetchBoards = async () => {
  try {
    const { data } = await boardListAPI()
    return data
  } catch (error) {
    console.log(error)
  }
}

const fetchBoardMemberships = async () => {
  try {
    const { data } = await boardMembershipsAPI()
    return data
  } catch (error) {
    console.log(error)
  }
}

const redirectToBoardTasks = (boardId) => {
  router.push({ name: 'boards-detail', params: { boardId } })
}

const loadBoards = async () => {
  const boards = await fetchBoards()

  dashboardStore.setBoards(boards)
}

onMounted(() => {
  loadBoards()
})


</script>

<template>
  <a-flex align="center" :gap="16">
    <a-button :icon="h(PlusOutlined)" type="primary" @click="showBoardNewModal"
      >New board</a-button
    >
    <a-button>New workspace</a-button>
    <a-input-search
      v-model:value="searchValue"
      placeholder="Search for a board"
      style="width: 300px"
      @search="onBoardSearch"
    />
  </a-flex>

  <div
    v-for="workspace in dashboardStore.workspaces"
    :key="workspace.id"
    style="margin-top: 20px"
  >
    <a-typography-title :level="5">{{ workspace.name }}</a-typography-title>

    <a-row :gutter="16">
      <a-col
        :span="6"
        v-for="board in dashboardStore.getBoardsFromWorkspaceId(workspace.id)"
      >
        <a-card
          size="small"
          @click="redirectToBoardTasks(board.id)"
          class="board-item"
        >
          <a-typography-text strong>{{ board.name }}</a-typography-text>
        </a-card>
      </a-col>
    </a-row>
  </div>

  <a-modal v-model:open="boardNewModal" title="New Board" :footer="null">
    <BoardNew @close="closeBoardNewModal" />
  </a-modal>
</template>

<style scoped>
.board-item {
  cursor: pointer;
}
</style>
