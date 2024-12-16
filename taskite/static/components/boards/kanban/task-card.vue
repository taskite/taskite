<script setup>
import { Avatar, AvatarGroup, Tag } from 'ant-design-vue'
import { generateAvatar } from '@/utils/helpers'
import TaskTypeIcon from '@/components/icons/task-type-icon.vue'
import { ClockCircleOutlined, FlagOutlined } from '@ant-design/icons-vue'

const props = defineProps(['board', 'task'])
</script>

<template>
  <div class="flex justify-between items-center">
    <div class="text-xs font-semibold mb-1">
      <TaskTypeIcon :taskType="props.task.taskType" />
      <span class="ml-1">{{ props.task.name }}</span>
    </div>

    <div
      v-if="props.board.isEstimateEnabled && !!props.task.estimate"
      class="flex gap-1"
    >
      <ClockCircleOutlined class="text-xs" />
      <div class="text-xs font-semibold">{{ props.task.estimate?.value }}</div>
    </div>
  </div>
  <div>{{ props.task.summary }}</div>

  <div class="mt-2 flex justify-between items-center">
    <Tag
      :bordered="false"
      class="text-xs font-semibold"
      v-if="!!props.task.priority"
    >
      <FlagOutlined />
      <span>{{ props.task?.priority.name }}</span>
    </Tag>
    <AvatarGroup size="small">
      <Avatar
        v-for="assignee in props.task.assignees"
        :key="assignee.id"
        :size="22"
        class="mr-1"
        :src="
          !!assignee.avatar
            ? assignee.avatar
            : generateAvatar(assignee.firstName)
        "
      />
    </AvatarGroup>
  </div>
</template>
