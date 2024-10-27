<script setup>
import { onMounted, ref } from 'vue';
import { taskListAPI } from '@/utils/api';
import { handleResponseError } from '@/utils/helpers';
import TaskTypeIcon from '@/components/icons/task-type-icon.vue';

const props = defineProps(['boardId', 'taskId'])

const tasks = ref([])
const loadSubTasks = async () => {
    try {
        const { data } = await taskListAPI(props.boardId, { parentId: props.taskId })
        tasks.value = data
    } catch (error) {
        handleResponseError(error)
    }
}

onMounted(() => {
    loadSubTasks()
})
</script>

<template>
<div v-if="tasks.length > 0" class="mb-2">
    <div class="text-lg font-semibold">Subtasks</div>
    <div class="flex flex-col">
        <div class="px-3 py-1 hover:bg-gray-100" v-for="task in tasks" :key="task.id">
            <div class="grid grid-cols-12 cursor-pointer">
                <div class="col-span-1"><TaskTypeIcon :taskType="task.taskType" /></div>
                <div class="col-span-2">{{ task.name }}</div>
                <div class="col-span-6">{{ task.summary }}</div>
            </div>
        </div>
    </div>
</div>
</template>