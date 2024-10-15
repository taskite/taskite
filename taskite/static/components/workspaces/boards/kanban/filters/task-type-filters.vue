<script setup>
import { Checkbox, CheckboxGroup } from 'ant-design-vue';
import { useKanbanStore } from '@/stores/kanban';
import { CheckSquareTwoTone, PlaySquareTwoTone, DownSquareTwoTone, PlusSquareTwoTone } from '@ant-design/icons-vue';

const store = useKanbanStore()
</script>

<template>
    <CheckboxGroup v-model:value="store.taskTypes" class="">
        <div class="flex flex-col gap-1">
            <div class="flex items-center gap-1">
                <Checkbox value="issue"></Checkbox>
                <CheckSquareTwoTone two-tone-color="#8B5CF6" />
                <div>Issue</div>
            </div>

            <div class="flex items-center gap-1">
                <Checkbox value="feature"></Checkbox>
                <PlusSquareTwoTone two-tone-color="#8B5CF6" />
                <div>Feature</div>
            </div>

            <div class="flex items-center gap-1">
                <Checkbox value="story"></Checkbox>
                <PlaySquareTwoTone two-tone-color="#8B5CF6" />
                <div>Story</div>
            </div>

            <div class="flex items-center gap-1">
                <Checkbox value="bug"></Checkbox>
                <DownSquareTwoTone two-tone-color="#8B5CF6" />
                <div>Bug</div>
            </div>
        </div>
    </CheckboxGroup>
</template>