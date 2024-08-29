<script setup>
import { useDashboardStore } from '@/stores/dashboard'
import { boardMembershipAPI, createBoardAPI } from '@/utils/api';
import { PlusOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue';
import { h, ref } from 'vue'

const emit = defineEmits(['close'])

const boardNewForm = ref({
  workspaceId: '',
  name: '',
  description: '',
})

const dashboardStore = useDashboardStore()

const setBoard = async (boardData) => {
    try {
        const { data } = await boardMembershipAPI(boardData.id)
        dashboardStore.addBoard({
            ...boardData,
            membership: data
        })

        // Emit close model
        emit('close')        
    } catch (error) {
        console.log(error)
    }
}

const submitForm = async (values) => {
  try {
    const { data } = await createBoardAPI(values)
    message.success('Board created successfully!')
    setBoard(data)
  } catch (error) {
    console.log(error)
  }
}

</script>

<template>
  <a-form
    name="board-new-form"
    :model="boardNewForm"
    layout="vertical"
    @finish="submitForm"
  >
    <a-row :gutter="16">
      <a-col :span="12">
        <a-form-item label="Workspace" name="workspaceId">
          <a-select v-model:value="boardNewForm.workspaceId">
            <a-select-option
              v-for="workspace in dashboardStore.allowedWorkspaces"
              :value="workspace.id"
            >
              {{ workspace.name }}
            </a-select-option>
          </a-select>
        </a-form-item>
      </a-col>
      <a-col :span="12">
        <a-form-item label="Name" name="name">
          <a-input v-model:value="boardNewForm.name" />
        </a-form-item>
      </a-col>
    </a-row>

    <a-form-item label="Description" name="description">
      <a-textarea v-model:value="boardNewForm.description" :rows="4" />
    </a-form-item>

    <a-form-item>
      <a-button type="primary" :icon="h(PlusOutlined)" html-type="submit">Create</a-button>
    </a-form-item>
  </a-form>
</template>

<style scoped></style>
