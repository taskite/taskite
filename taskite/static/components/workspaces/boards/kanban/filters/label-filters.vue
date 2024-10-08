<script setup>
import { Checkbox, CheckboxGroup, Tag } from 'ant-design-vue';
import { useKanbanStore } from '@/stores/kanban';
import { TagTwoTone } from '@ant-design/icons-vue';

const store = useKanbanStore()
</script>

<template>
    <CheckboxGroup v-model:value="store.labelFilters" class="">
        <div class="flex flex-col gap-1">
            <div class="flex items-center gap-2" v-for="label in store.labels" :key="label.id">
                <Checkbox :value="label.id"></Checkbox>
                <div>
                    <TagTwoTone :two-tone-color="label.color" />
                    <span class="ml-2">
                        {{ label.name }}
                    </span>
                </div>
            </div>
        </div>
    </CheckboxGroup>
</template>