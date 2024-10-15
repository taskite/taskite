<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue';
import { Skeleton, Statistic, Card, Table } from 'ant-design-vue';
import { ref, computed, onMounted } from 'vue'
import { boardStatsAPI } from '@/utils/api';
import { handleResponseError } from '@/utils/helpers';
import TaskList from './task-list.vue';

const props = defineProps(['workspace', 'currentUser'])

const currentDateTime = ref(new Date())

const greeting = computed(() => {
    const hour = currentDateTime.value.getHours()
    if (hour < 12) return 'Good morning'
    if (hour < 18) return 'Good afternoon'
    return 'Good evening'
})

const formattedDateTime = computed(() => {
    const options = { weekday: 'long', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }
    return currentDateTime.value.toLocaleDateString('en-US', options)
})

const updateDateTime = () => {
    currentDateTime.value = new Date()
}

const stats = ref({
    assignedTasksCount: 0,
    createdTasksCount: 0,
    recentTasksAssigned: [],
    recentTasksCreated: []
})
const loadStats = async () => {
    try {
        const { data } = await boardStatsAPI(props.workspace.id)
        stats.value.assignedTasksCount = data.assignedTasksCount
        stats.value.createdTasksCount = data.createdTasksCount

        stats.value.recentTasksAssigned = data.recentTasksAssigned.map(item => ({ ...item, key: item.id }))
        stats.value.recentTasksCreated = data.recentTasksCreated.map(item => ({ ...item, key: item.id }))
    } catch (error) {
        handleResponseError(error)
    }
}

onMounted(() => {
    updateDateTime()
    // Update time every minute
    setInterval(updateDateTime, 60000)

    loadStats()
})
</script>

<template>
    <WorkspaceLayout :workspace="props.workspace" page="dashboard" :currentUser="props.currentUser">
        <div class="p-4">
            <div class="flex justify-between">
                <div>
                    <div class="text-lg font-bold">
                        {{ greeting }},
                        {{ props.currentUser.firstName }} {{ props.currentUser?.lastName }}
                    </div>
                    <div class="text-gray-500">
                        <span>{{ greeting === 'Good morning' ? '☀️' : '🌤️' }}</span>
                        {{ formattedDateTime }}
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-2 mt-5 gap-5" v-if="!!stats">
                <Card>
                    <Statistic title="Tasks assigned" :value="stats.assignedTasksCount" />
                    <div>Recently assigned tasks</div>
                    <TaskList :tasks="stats.recentTasksAssigned" />
                </Card>

                <Card>
                    <Statistic title="Tasks created" :value="stats.createdTasksCount" />
                    <div>Recently created tasks</div>
                    <TaskList :tasks="stats.recentTasksCreated" />
                </Card>
            </div>

            <Skeleton v-else />
        </div>
    </WorkspaceLayout>
</template>

<style scoped></style>