<script setup>
import { Checkbox, CheckboxGroup } from 'ant-design-vue';
import { useKanbanStore } from '@/stores/kanban';

const store = useKanbanStore()
</script>

<template>
    <CheckboxGroup v-model:value="store.taskTypes" class="">
        <div class="flex flex-col gap-1">
            <div class="flex items-center gap-2">
                <Checkbox value="issue"></Checkbox>
                <div>Issue</div>
            </div>

            <div class="flex items-center gap-2">
                <Checkbox value="feature"></Checkbox>
                <div>Feature</div>
            </div>

            <div class="flex items-center gap-2">
                <Checkbox value="story"></Checkbox>
                <div>Story</div>
            </div>

            <div class="flex items-center gap-2">
                <Checkbox value="bug"></Checkbox>
                <div>Bug</div>
            </div>
        </div>
    </CheckboxGroup>
</template>