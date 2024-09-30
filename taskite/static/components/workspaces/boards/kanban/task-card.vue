<script setup>
import { Avatar, AvatarGroup, Card } from 'ant-design-vue';
import { generateAvatar } from '@/utils/helpers';

const props = defineProps(['boardId', 'task'])
</script>

<template>
    <Card size="small" class="rounded">
        <div class="text-xs font-semibold mb-1">{{ props.task.name }}</div>
        <div>{{ props.task.summary }}</div>

        <div class="mt-2">
            <AvatarGroup size="small">
                <Avatar v-for="assignee in props.task.assignees" :key="assignee.id" size="small"
                    :src="!!assignee.avatar ? assignee.avatar : generateAvatar(assignee.firstName)" />
            </AvatarGroup>
        </div>
    </Card>
</template>