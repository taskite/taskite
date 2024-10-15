<script setup>
import { Avatar, AvatarGroup, Card } from 'ant-design-vue';
import { generateAvatar } from '@/utils/helpers';
import { CheckSquareTwoTone, PlaySquareTwoTone, DownSquareTwoTone, PlusSquareTwoTone } from '@ant-design/icons-vue';

const props = defineProps(['boardId', 'task'])
</script>

<template>
    <div class="text-xs font-semibold mb-1">
        <CheckSquareTwoTone two-tone-color="#8B5CF6" v-if="task.taskType === 'issue'" />
        <PlaySquareTwoTone two-tone-color="#8B5CF6" v-else-if="task.taskType === 'story'" />
        <DownSquareTwoTone two-tone-color="#8B5CF6" v-else-if="task.taskType === 'bug'" />
        <PlusSquareTwoTone two-tone-color="#8B5CF6" v-else-if="task.taskType === 'feature'" />
        <span class="ml-1">{{ props.task.name }}</span>
    </div>
    <div>{{ props.task.summary }}</div>

    <div class="mt-2 flex justify-end">
        <AvatarGroup size="small">
            <Avatar v-for="assignee in props.task.assignees" :key="assignee.id" :size="22" class="mr-1"
                :src="!!assignee.avatar ? assignee.avatar : generateAvatar(assignee.firstName)" />
        </AvatarGroup>
    </div>
</template>