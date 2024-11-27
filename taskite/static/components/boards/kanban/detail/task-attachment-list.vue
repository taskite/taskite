<script setup>
import { Avatar } from 'ant-design-vue';

const props = defineProps(['boardId', 'taskId', 'attachments'])
</script>

<template>
    <div v-if="props.attachments.length > 0">
        <div class="text-base font-semibold">Attachments</div>
        <div class="flex gap-2">
            <div v-for="attachment in props.attachments" :key="attachment.id">
                <Avatar :src="attachment.attachment" size="large"></Avatar>
            </div>
        </div>
    </div>
</template>