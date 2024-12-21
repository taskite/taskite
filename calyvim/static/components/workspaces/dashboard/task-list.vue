<script setup>
import { Table } from 'ant-design-vue';
import TaskTypeIcon from '@/components/icons/task-type-icon.vue';
const props = defineProps(['tasks'])

const columns = [
    {
        // title: 'Name',
        key: 'name'
    },
    {
        // title: 'Board',
        key: 'board'
    },
    {
        // title: 'Summary',
        key: 'summary'
    }
]
</script>

<template>
    <Table :columns="columns" :dataSource="props.tasks" :pagination="false" size="small">
        <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'name'">
                <div class="flex items-center gap-2">
                    <div>
                        <TaskTypeIcon :taskType="record.taskType" />
                    </div>
                    <div>
                        {{ record.name }}
                    </div>
                </div>
            </template>

            <template v-else-if="column.key === 'board'">
                <div>{{ record.board.name }}</div>
            </template>

            <template v-else-if="column.key === 'summary'">
                <div>{{ record.summary }}</div>
            </template>
        </template>
    </Table>
</template>