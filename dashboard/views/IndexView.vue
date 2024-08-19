<script setup>
import { useOrganizationStore } from '@/stores/organization'
import { boardListAPI, createBoardAPI } from '@/utils/api'
import { PlusOutlined } from '@ant-design/icons-vue'
import { ref, h, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router';

const router = useRouter()

const searchValue = ref('')
const onBoardSearch = (value) => {
  console.log(value)
}

const organizationStore = useOrganizationStore()

const boardNewModal = ref(false)
const showBoardNewModal = () => {
  boardNewModal.value = true
}
const closeBoardNewModal = () => {
  boardNewModal.value = false
}

const newBoardForm = ref({
  organizationId: '',
  name: '',
  description: '',
  visibility: 'private',
})

const onNewBoardFinish = async (values) => {
  try {
    const { data } = await createBoardAPI(values)
    boards.value.push(data)
    boardNewModal.value = false
  } catch (error) {
    console.log(error)
  }
}

const boards = ref([])
const fetchBoards = async () => {
  try {
    const { data } = await boardListAPI()
    boards.value = data
  } catch (error) {
    console.log(error)
  }
}

const groupedBoards = computed(() => {
  const organizations = organizationStore.organizations.map((organization) => {
    const boardList = boards.value.filter(
      (board) => board.organizationId === organization.id
    )

    return {
      ...organization,
      boards: boardList,
    }
  })

  return organizations
})

const redirectToBoardTasks = (boardId) => {
  router.push({ name: 'tasks', params: { boardId } })
}

onMounted(async () => {
  await fetchBoards()
})
</script>

<template>
  <a-flex align="center" :gap="16">
    <a-button :icon="h(PlusOutlined)" type="primary" @click="showBoardNewModal"
      >New board</a-button
    >
    <a-button>New organization</a-button>
    <a-input-search
      v-model:value="searchValue"
      placeholder="Search for a board"
      style="width: 300px"
      @search="onBoardSearch"
    />
  </a-flex>

  <div v-for="org in groupedBoards" :key="org.id" style="margin-top: 20px">
    <a-typography-title :level="5">{{ org.name }}</a-typography-title>

    <a-row :gutter="16">
      <a-col :span="6" v-for="board in org.boards">
        <a-card size="small" @click="redirectToBoardTasks(board.id)" class="board-item">
          <a-typography-text strong>{{ board.name }}</a-typography-text>
        </a-card>
      </a-col>
    </a-row>
  </div>

  <a-modal v-model:open="boardNewModal" title="New board" :footer="null">
    <a-form
      :model="newBoardForm"
      name="newBoardForm"
      @finish="onNewBoardFinish"
      layout="vertical"
      hideRequiredMark
    >
      <a-form-item label="Organization" name="organizationId">
        <a-select v-model:value="newBoardForm.organizationId">
          <a-select-option
            :value="organization.id"
            v-for="organization in organizationStore.organizations"
            :key="organization.id"
          >
            {{ organization.name }}
          </a-select-option>
        </a-select>
      </a-form-item>

      <a-form-item
        label="Name"
        name="name"
        :rules="[{ required: true, message: 'Please input board name!' }]"
      >
        <a-input v-model:value="newBoardForm.name"></a-input>
      </a-form-item>

      <a-form-item label="Visibility" name="visibility">
        <a-select v-model:value="newBoardForm.visibility">
          <a-select-option value="private">Private</a-select-option>
          <a-select-option value="public">Public</a-select-option>
        </a-select>
      </a-form-item>

      <a-form-item label="Description" name="description">
        <a-textarea
          v-model:value="newBoardForm.description"
          :rows="4"
        ></a-textarea>
      </a-form-item>

      <a-flex justify="space-between">
        <a-form-item>
          <a-button @click="closeBoardNewModal">Cancel</a-button>
        </a-form-item>

        <a-form-item>
          <a-button type="primary" :icon="h(PlusOutlined)" html-type="submit"
            >Create board</a-button
          >
        </a-form-item>
      </a-flex>
    </a-form>
  </a-modal>
</template>

<style scoped>
.board-item {
  cursor: pointer;
}
</style>