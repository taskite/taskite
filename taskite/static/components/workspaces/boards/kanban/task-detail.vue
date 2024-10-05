<script setup>
import { Avatar, Input, Select, SelectOption, Textarea } from 'ant-design-vue';
import { onMounted, ref } from 'vue';
import { useKanbanStore } from '@/stores/kanban';
import { generateAvatar, handleResponseError } from '@/utils/helpers';
import { taskUpdateAPI } from '@/utils/api';

const props = defineProps(['boardId', 'task'])
const store = useKanbanStore()

const taskForm = ref({
    summary: props.task.summary,
    description: props.task.description,
    priorityId: props.task.priorityId,
    stateId: props.task.stateId,
    assignees: props.task.assignees.map(assignee => assignee.id),
})

const updateTask = async (updatedData) => {
    try {
        const { data } = await taskUpdateAPI(props.boardId, props.task.id, updatedData)
        store.updateTask(props.task.stateId, props.task.id, data)
    } catch (error) {
        handleResponseError(error)
    }
}

const updateSummary = (event) => {
    if(event.target.value === props.task.summary) return

    // Update the task
    updateTask({ summary: event.target.value })
}

const updatePriority = (priorityId) => {
    if(priorityId === props.task.priorityId) return

    // Update the task
    updateTask({ priorityId: priorityId })
}

const updateAssignees = (assignees) => {
    
    // Update the task
    updateTask({ assignees })
}

const updateState = (stateId) => {
    // Update the task
    updateTask({ stateId })
    taskForm.value.stateId = stateId
}

onMounted(() => {

})
</script>

<template>
    <div class="grid grid-cols-12 gap-6">
        <div class="col-span-8">
            <div>{{ props.task.name }}</div>
            <Input :bordered="false" v-model:value="taskForm.summary" @blur="updateSummary" />

            <div class="mt-2">
                <div>Description</div>
                <Textarea v-model:value="taskForm.description" :rows="7" />
            </div>
        </div>

        <div class="col-span-4">
            <div class="flex items-center gap-2 mb-2">
                <div>Created by </div>
                <Avatar size="small" shape="square"
                    :src="!!props.task.createdBy.avatar ? props.task.createdBy.avatar : generateAvatar(props.task.createdBy.firstName)" />
                <div>{{ props.task.createdBy.firstName }} {{ props.task.createdBy?.lastName }}</div>
            </div>
            <Select v-model:value="taskForm.stateId" class="w-52 mb-2" @change="updateState">
                <SelectOption :value="state.id" v-for="state in store.states" :key="state.id">{{ state.name }}
                </SelectOption>
            </Select>

            <div class="mb-2">
                <div class="font-semibold mb-1">Properties</div>
                <div class="flex flex-col gap-2">
                    <div>Priority</div>
                    <Select v-model:value="taskForm.priorityId" @change="updatePriority">
                        <SelectOption :value="null">None</SelectOption>
                        <SelectOption :value="priority.id" v-for="priority in store.priorities" :key="priority.id">
                            {{ priority.name }}
                        </SelectOption>
                    </Select>
                </div>

                <div class="flex flex-col gap-2">
                    <div>Assignees</div>
                    <Select v-model:value="taskForm.assignees" mode="multiple"
                        optionFilterProp="label" @change="updateAssignees">
                        <SelectOption v-for="member in store.members" :key="member.id" :label="member.firstName">
                            <div class="flex items-center gap-2">
                                <Avatar size="small"
                                    :src="!!member.avatar ? member.avatar : generateAvatar(member.firstName)" />
                                <div>{{ member.firstName }} {{ member?.lastName }}</div>
                            </div>
                        </SelectOption>
                    </Select>
                </div>
            </div>
        </div>
    </div>
</template>