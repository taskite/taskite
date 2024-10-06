<script setup>
import { Avatar, Input, Select, SelectOption, Textarea, Skeleton } from 'ant-design-vue';
import { onMounted, ref } from 'vue';
import { useKanbanStore } from '@/stores/kanban';
import { generateAvatar, handleResponseError } from '@/utils/helpers';
import { taskUpdateAPI, taskDetailAPI } from '@/utils/api';

const props = defineProps(['boardId', 'taskId'])
const store = useKanbanStore()

const task = ref(null)

const updateTask = async (updatedData) => {
    try {
        const { data } = await taskUpdateAPI(props.boardId, props.taskId, updatedData)
        store.updateTask(data)
        return data
    } catch (error) {
        handleResponseError(error)
    }
}

const updatePriority = (priorityId) => {
    // Update the task
    updateTask({ priorityId: priorityId })
}

const updateAssignees = async (assignees) => {

    // Update the task
    updateTask({ assignees })
}

const updateState = async (stateId) => {
    // Update the task
    try {
        const { data } = await taskUpdateAPI(props.boardId, props.taskId, { stateId })
        store.updateTaskState(task.value.oldStateId, data)
        task.value = {
            ...data,
            assigneeIds: data.assignees.map(assignee => assignee.id),
            oldStateId: data.stateId
        }
    } catch (error) {
        handleResponseError(error)
    }
}

const fetchTask = async () => {
    try {
        const { data } = await taskDetailAPI(props.boardId, props.taskId)
        task.value = {
            ...data,
            assigneeIds: data.assignees.map(assignee => assignee.id),
            oldStateId: data.stateId
        }
    } catch (error) {
        handleResponseError(error)
    }
}

onMounted(() => {
    fetchTask()
})
</script>

<template>
    <div class="grid grid-cols-12 gap-6" v-if="!!task">
        <div class="col-span-8">
            <div>{{ task.name }}</div>
            <Input :bordered="false" v-model:value="task.summary"
                @keyup.enter="(event) => updateTask({ summary: event.target.value })" />

            <div class="mt-2">
                <div>Description</div>
                <!-- <DescriptionEditor v-model:value="task.description" /> -->
                <Textarea v-model:value="task.description" :rows="15"
                    @keyup.enter="(event) => updateTask({ description: event.target.value })" />
            </div>
        </div>

        <div class="col-span-4">
            <div class="flex items-center gap-2 mb-2">
                <div>Created by </div>
                <Avatar size="small" shape="square"
                    :src="!!task.createdBy.avatar ? task.createdBy.avatar : generateAvatar(task.createdBy.firstName)" />
                <div>{{ task.createdBy.firstName }} {{ task.createdBy?.lastName }}</div>
            </div>
            <Select v-model:value="task.stateId" class="w-52 mb-2" @change="updateState">
                <SelectOption :value="state.id" v-for="state in store.states" :key="state.id">{{ state.name }}
                </SelectOption>
            </Select>

            <div class="mb-2">
                <div class="font-semibold mb-1">Properties</div>
                <div class="flex flex-col gap-2">
                    <div>Priority</div>
                    <Select v-model:value="task.priorityId" @change="updatePriority">
                        <SelectOption :value="null">None</SelectOption>
                        <SelectOption :value="priority.id" v-for="priority in store.priorities" :key="priority.id">
                            {{ priority.name }}
                        </SelectOption>
                    </Select>
                </div>

                <div class="flex flex-col gap-2">
                    <div>Assignees</div>
                    <Select v-model:value="task.assigneeIds" mode="multiple" optionFilterProp="label"
                        @change="updateAssignees">
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
    <div v-else>
        <Skeleton />
    </div>
</template>