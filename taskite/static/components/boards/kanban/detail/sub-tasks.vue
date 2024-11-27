<script setup>
import { h, onMounted, ref } from 'vue'
import { taskListAPI } from '@/utils/api'
import { handleResponseError } from '@/utils/helpers'
import TaskTypeIcon from '@/components/icons/task-type-icon.vue'
import { useKanbanStore } from '@/stores/kanban'
import {
  Button,
  FormItem,
  Input,
  List,
  Form,
  ListItem,
  Select,
  SelectOption,
} from 'ant-design-vue'
import { PlusOutlined } from '@ant-design/icons-vue'

const props = defineProps(['boardId', 'taskId', 'showSubtaskAddForm'])
const emit = defineEmits(['added', 'close'])

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

const addForm = ref({
  summary: '',
  taskType: 'issue',
  stateId: store.states[0].id
})

const dummyTasks = ref(['add-form'])

const onFinish = (values) => {
  emit('added', values)
}

onMounted(() => {
  loadSubTasks()
})
</script>

<template>
  <div class="mb-2" v-if="tasks.length > 0">
    <div class="text-base font-semibold">Subtasks</div>
    <List item-layout="horizontal" :data-source="tasks">
      <template #renderItem="{ item }">
        <ListItem
          class="hover:bg-gray-100 flex items-center justify-between px-2 py-2"
        >
          <div
            class="flex items-center gap-2 cursor-pointer"
            @click="openSubTask(item.id)"
          >
            <TaskTypeIcon :taskType="item.taskType" />
            <span>{{ item.name }}</span>
            <!-- Long Title Handling -->
            <div class="text-sm text-gray-800 break-words line-clamp-2">
              {{ item.summary }}
            </div>
          </div>

          <div class="flex items-center gap-4">
            <span>{{ item?.priority?.name }}</span>

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

    <List item-layout="horizontal" :data-source="dummyTasks" v-if="props.showSubtaskAddForm">
      <template #renderItem="{ item }">
        <ListItem class="hover:bg-gray-100">
          <Form :model="addForm" class="w-full" layout="vertical" @finish="onFinish">
            <div class="grid grid-cols-12">
              <FormItem name="taskType" class="col-span-2">
                <Select v-model:value="addForm.taskType" :bordered="false">
                  <SelectOption value="issue">
                    <TaskTypeIcon taskType="issue" />
                    <span class="ml-1">Issue</span>
                  </SelectOption>
                  <SelectOption value="bug">
                    <TaskTypeIcon taskType="bug" />
                    <span class="ml-1">Bug</span>
                  </SelectOption>
                  <SelectOption value="story">
                    <TaskTypeIcon taskType="story" />
                    <span class="ml-1">Story</span>
                  </SelectOption>
                  <SelectOption value="feature">
                    <TaskTypeIcon taskType="feature" />
                    <span class="ml-1">Feature</span>
                  </SelectOption>
                </Select>
              </FormItem>

              <FormItem name="summary" class="col-span-6">
                <Input
                  placeholder="What is the task about ?"
                  :bordered="false"
                  v-model:value="addForm.summary"
                />
              </FormItem>
              
              <FormItem name="stateId" class="col-span-4">
                <Select v-model:value="addForm.stateId" :bordered="false">
                  <SelectOption v-for="state in store.states" :value="state.id" :key="state.id">{{ state.name }}</SelectOption>
                </Select>
              </FormItem>
            </div>

            <div class="flex justify-end gap-2">
              <FormItem>
                <Button type="primary" html-type="submit">Create</Button>
              </FormItem>
              <Button @click="emit('close')">Cancel</Button>
            </div>
          </Form>
        </ListItem>
      </template>
    </List>
  </div>
</template>
