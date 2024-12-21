<script setup>
import { Checkbox, CheckboxGroup } from 'ant-design-vue';
import { useKanbanStore } from '@/stores/kanban';
import { FlagOutlined } from '@ant-design/icons-vue';

const store = useKanbanStore()
</script>

<template>
    <CheckboxGroup v-model:value="store.priorityFilters" class="">
        <div class="flex flex-col gap-1">
            <div class="flex items-center gap-2" v-for="priority in store.priorities" :key="priority.id">
                <Checkbox :value="priority.id"></Checkbox>
                <div>
                    <FlagOutlined />
                    <span class="ml-2">{{ priority.name }}</span>
                </div>
            </div>
        </div>
    </CheckboxGroup>
</template>