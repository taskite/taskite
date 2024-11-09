<script setup>
import { h, onMounted, ref } from 'vue'
import { taskListAPI } from '@/utils/api'
import { handleResponseError } from '@/utils/helpers'
import TaskTypeIcon from '@/components/icons/task-type-icon.vue'
import { useKanbanStore } from '@/stores/kanban'
import { Button, List, ListItem, Select, SelectOption } from 'ant-design-vue'
import { PlusOutlined } from '@ant-design/icons-vue'

const props = defineProps(['boardId', 'taskId'])

const store = useKanbanStore()

const tasks = ref([])
const loadSubTasks = async () => {
  try {
    const { data } = await taskListAPI(props.boardId, {
      parentId: props.taskId,
    })
    tasks.value = data
  } catch (error) {
    handleResponseError(error)
  }
}

const openSubTask = (taskId) => {
  store.setSelectedTask(taskId)
}

onMounted(() => {
  loadSubTasks()
})
</script>

<template>
  <div class="mb-2">
    <div class="flex justify-between">
      <div class="text-lg font-semibold">Subtasks</div>
      <Button :icon="h(PlusOutlined)" size="small" type="primary">Add subtask</Button>
    </div>
    <List item-layout="horizontal" :data-source="tasks">
      <template #renderItem="{ item }">
        <ListItem
          class="hover:bg-gray-100 flex items-center justify-between px-4 py-2"
        >
          <div class="flex items-center gap-2 cursor-pointer" @click="openSubTask(item.id)">
            <TaskTypeIcon :taskType="item.taskType" />
            <span>{{ item.name }}</span>
            <!-- Long Title Handling -->
            <div class="text-sm text-gray-800 break-words line-clamp-2">
              {{ item.summary }}
            </div>
          </div>

          <div class="flex items-center gap-4">
            <span>{{ item.priority.name }}</span>

            <Select v-model:value="item.stateId" class="w-28">
              <SelectOption
                :value="state.id"
                v-for="state in store.states"
                :key="state.id"
              >
                {{ state.name }}
              </SelectOption>
            </Select>
          </div>
        </ListItem>
      </template>
    </List>
  </div>
</template>
