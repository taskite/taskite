<script setup>
import { Card, Divider } from 'ant-design-vue';

import TaskTypeFilters from './task-type-filters.vue';
import AssigneeFilters from './assignee-filters.vue';
import PriorityFilters from './priority-filters.vue';
</script>

<template>
    <Card class="w-80" title="Filters" size="small">
        <div>
            <div class="font-semibold text-gray-600">Priorities</div>
            <PriorityFilters />
        </div>

        <Divider class="my-2 p-0" />

        <div>
            <div class="font-semibold text-gray-600">Assignees</div>
            <AssigneeFilters />
        </div>

        <Divider class="my-2 p-0" />

        <div>
            <div class="font-semibold text-gray-600">Types</div>
            <TaskTypeFilters />
        </div>        
    </Card>
</template>