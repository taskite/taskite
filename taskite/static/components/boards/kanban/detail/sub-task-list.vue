<script setup>
import { useKanbanStore } from '@/stores/kanban'
import { Divider, Select, SelectOption } from 'ant-design-vue'
import TaskTypeIcon from '@/components/icons/task-type-icon.vue'
import { handleResponseError } from '@/utils/helpers'
import { taskUpdateAPI } from '@/utils/api'

const props = defineProps(['subtasks', 'boardId'])
const store = useKanbanStore()

const handleStateChange = async (value, taskId) => {
  try {
    await taskUpdateAPI(props.boardId, taskId, { stateId: value })
  } catch (error) {
    handleResponseError(error)
  }
}

const openSubTask = (taskId) => {
    store.setSelectedTask(taskId)
}
</script>

<template>
  <div v-if="props.subtasks.length > 0">
    <Divider />
    <div class="text-lg font-semibold">Subtasks</div>
    <div v-for="task in props.subtasks" :key="task.id">
      <div class="flex justify-between items-center px-3 py-2 rounded shadow">
        <div class="flex gap-2 items-center">
          <TaskTypeIcon :taskType="task.taskType" />
          <div
            class="font-semibold hover:underline hover:underline-offset-1 text-primary cursor-pointer"
            @click="openSubTask(task.id)"
          >
            {{ task.name }}
          </div>
          <div
            class="font-semibold hover:underline hover:underline-offset-1 cursor-pointer"
            @click="openSubTask(task.id)"
          >
            {{ task.summary }}
          </div>
        </div>
        <div class="flex gap-2 items-center">
          <div class="text-xs font-semibold">{{ task?.priority?.name }}</div>
          <Select
            v-model:value="task.stateId"
            size="small"
            style="width: 100px"
            @change="(value) => handleStateChange(value, task.id)"
          >
            <SelectOption
              :value="state.id"
              v-for="state in store.states"
              :key="state.id"
              >{{ state.name }}
            </SelectOption>
          </Select>
        </div>
      </div>
    </div>
  </div>
</template>
