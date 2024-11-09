<script setup>
import { Avatar, Divider, Select, SelectOption } from 'ant-design-vue'
import { generateAvatar } from '@/utils/helpers'
import { useKanbanStore } from '@/stores/kanban'

const props = defineProps(['task'])
const emit = defineEmits(['updateProperties', 'updateState'])

const store = useKanbanStore()

const getAvatarSrc = (memberId) => {
  const member = store.members.find((m) => m.id === memberId)
  return member ? member.avatar || generateAvatar(member.firstName) : ''
}
</script>

<template>
  <div class="mb-2 font-semibold">Status</div>
  <Select
    v-model:value="task.stateId"
    class="w-full mb-2"
    @change="(stateId) => emit('updateState', stateId)"
  >
    <SelectOption
      :value="state.id"
      v-for="state in store.states"
      :key="state.id"
    >
      {{ state.name }}
    </SelectOption>
  </Select>

  <Divider class="p-0 my-3" />

  <div class="mb-2 font-semibold">Assignees</div>
  <Select
    v-model:value="task.assigneeIds"
    mode="multiple"
    optionFilterProp="label"
    @change="(assigneeIds) => emit('updateProperties', { assigneeIds })"
    class="w-full"
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
            !!member.avatar ? member.avatar : generateAvatar(member.firstName)
          "
        />
        <div>{{ member.firstName }} {{ member?.lastName }}</div>
      </div>
    </SelectOption>
  </Select>

  <Divider class="p-0 my-3" />

  <div class="mb-2 font-semibold">Task type</div>
  <Select
    v-model:value="task.taskType"
    class="w-full"
    @change="(taskType) => emit('updateProperties', { taskType })"
  >
    <SelectOption value="issue"> Issue </SelectOption>
    <SelectOption value="bug"> Bug </SelectOption>
    <SelectOption value="story"> Story </SelectOption>
    <SelectOption value="feature"> Feature </SelectOption>
  </Select>

  <Divider class="p-0 my-3" />

  <div class="mb-2 font-semibold">Priority</div>

  <Select
    v-model:value="task.priorityId"
    @change="(priorityId) => emit('updateProperties', { priorityId })"
    class="w-full"
  >
    <SelectOption :value="null">None</SelectOption>
    <SelectOption
      :value="priority.id"
      v-for="priority in store.priorities"
      :key="priority.id"
    >
      {{ priority.name }}
    </SelectOption>
  </Select>
</template>

<style scoped></style>
