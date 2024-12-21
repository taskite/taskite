<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue';
import { Skeleton, Statistic, Card, Table } from 'ant-design-vue';
import { ref, computed, onMounted } from 'vue'
import { boardStatsAPI } from '@/utils/api';
import { handleResponseError } from '@/utils/helpers';
import TaskList from './task-list.vue';
import TasksHeatmap from './tasks-heatmap.vue';

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
    recentTasksCreated: [],
    taskContributions: null
})
const loadStats = async () => {
    try {
        const { data } = await boardStatsAPI(props.workspace.id)
        stats.value.assignedTasksCount = data.assignedTasksCount
        stats.value.createdTasksCount = data.createdTasksCount

        stats.value.recentTasksAssigned = data.recentTasksAssigned.map(item => ({ ...item, key: item.id }))
        stats.value.recentTasksCreated = data.recentTasksCreated.map(item => ({ ...item, key: item.id }))

        const taskContributions = {}
        data.taskContributions.forEach(c => {
            taskContributions[c.day] = c.taskCount
        })
        stats.value.taskContributions = taskContributions
        // stats.value.taskContributions = data.taskContributions
    } catch (error) {
        handleResponseError(error)
    }
}

const taskData = {
    "2024-01-01": 5,
    "2024-01-02": 2,
    "2024-01-03": 7,
    "2024-01-05": 4,
    "2024-01-06": 1,
    "2024-01-10": 8,
    "2024-02-01": 3,
    "2024-02-15": 6,
    "2024-03-10": 12,
    "2024-03-21": 9,
    "2024-04-05": 4,
    "2024-04-25": 10,
    "2024-05-15": 5,
    "2024-06-01": 2,
    "2024-07-20": 7,
    "2024-08-30": 3,
    "2024-09-15": 11,
    "2024-10-10": 4,
    "2024-11-01": 9,
    "2024-12-25": 15,
    "2024-12-31": 10,
};

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

            <div class="flex items-center justify-between">
                <div class="flex gap-4">
                    <Statistic title="Tasks assigned" :value="stats.assignedTasksCount" />
                    <Statistic title="Tasks created" :value="stats.createdTasksCount" />
                </div>
                <div>
                    <div class="text-lg">Task Contributions</div>
                    <TasksHeatmap :data="stats.taskContributions" v-if="!!stats.taskContributions" />
                </div>
            </div>


            <div class="grid grid-cols-2 mt-5 gap-5" v-if="!!stats">
                <Card>
                    <div>Recently assigned tasks</div>
                    <TaskList :tasks="stats.recentTasksAssigned" />
                </Card>

                <Card>

                    <div>Recently created tasks</div>
                    <TaskList :tasks="stats.recentTasksCreated" />
                </Card>
            </div>

            <Skeleton v-else />
        </div>
    </WorkspaceLayout>
</template>

<style scoped></style>