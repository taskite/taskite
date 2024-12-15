<script setup>
import { useKanbanStore } from '@/stores/kanban'
import {
  Form,
  FormItem,
  Input,
  Textarea,
  Select,
  SelectOption,
  Avatar,
  Button,
} from 'ant-design-vue'
import { h, ref } from 'vue'
import { generateAvatar, handleResponseError } from '@/utils/helpers'
import { PlusOutlined } from '@ant-design/icons-vue'
import { taskCreateAPI } from '@/utils/api'

const props = defineProps(['task', 'boardId'])
const emit = defineEmits(['created'])

const store = useKanbanStore()

const getAvatarSrc = (memberId) => {
  const member = store.members.find((m) => m.id === memberId)
  return member ? member.avatar || generateAvatar(member.firstName) : ''
}

const subTaskForm = ref({
  summary: '',
  description: '',
  taskType: 'issue',
  stateId: store.states.length > 0 ? store.states[0].id : '',
  assignees: [],
  priorityId: null,
})
const formRef = ref()

const onSubmit = async (values) => {
  try {
    const { data } = await taskCreateAPI(props.boardId, {
      ...values,
      parentId: props.task.id,
    })
    formRef.value.resetFields()
    emit('created', data)
  } catch (error) {
    handleResponseError(error)
  }
}
</script>

<template>
  <Form :model="subTaskForm" layout="vertical" @finish="onSubmit" ref="formRef">
    <div class="grid grid-cols-4 gap-2">
      <div class="col-span-1">
        <FormItem name="stateId" label="State">
          <Select v-model:value="subTaskForm.stateId">
            <SelectOption
              :value="state.id"
              v-for="state in store.states"
              :key="state.id"
              >{{ state.name }}
            </SelectOption>
          </Select>
        </FormItem>
      </div>
      <div class="col-span-3">
        <FormItem
          name="summary"
          label="Summary"
          :rules="[{ required: true, message: 'Summary is required.' }]"
        >
          <Input v-model:value="subTaskForm.summary" />
        </FormItem>
      </div>
    </div>

    <FormItem name="description" label="Description">
      <Textarea v-model:value="subTaskForm.description" :rows="5" />
    </FormItem>

    <div class="grid grid-cols-3 gap-2">
      <FormItem name="taskType" label="Task type">
        <Select v-model:value="subTaskForm.taskType">
          <SelectOption value="issue">Issue</SelectOption>
          <SelectOption value="feature">Feature</SelectOption>
          <SelectOption value="story">Story</SelectOption>
          <SelectOption value="bug">Bug</SelectOption>
        </Select>
      </FormItem>
      <FormItem name="priorityId" label="Priority">
        <Select v-model:value="subTaskForm.priorityId">
          <SelectOption :value="null">None</SelectOption>
          <SelectOption
            :value="priority.id"
            v-for="priority in store.priorities"
            :key="priority.id"
          >
            {{ priority.name }}
          </SelectOption>
        </Select>
      </FormItem>

      <FormItem name="assignees" label="Assignees">
        <Select
          v-model:value="subTaskForm.assignees"
          mode="multiple"
          optionFilterProp="label"
        >
          <template #tagRender="{ value }">
            <Avatar size="small" :src="getAvatarSrc(value)" />
          </template>
          <SelectOption
            v-for="member in store.members"
            :key="member.id"
            :label="member.firstName"
          >
            <div class="flex items-center gap-2">
              <Avatar
                size="small"
                :src="
                  !!member.avatar
                    ? member.avatar
                    : generateAvatar(member.firstName)
                "
              />
              <div>{{ member.firstName }} {{ member?.lastName }}</div>
            </div>
          </SelectOption>
        </Select>
      </FormItem>
    </div>

    <div class="flex justify-end">
      <FormItem>
        <Button type="primary" :icon="h(PlusOutlined)" html-type="submit"
          >Create subtask</Button
        >
      </FormItem>
    </div>
  </Form>
</template>
