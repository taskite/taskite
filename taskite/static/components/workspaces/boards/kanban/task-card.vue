<script setup>
import { Card } from 'ant-design-vue';

const props = defineProps(['boardId', 'task'])
</script>

<template>
    <Card size="small" class="rounded">
        <div class="text-xs font-semibold mb-1">{{ props.task.name }}</div>
        <div>{{ props.task.summary }}</div>
    </Card>
</template>