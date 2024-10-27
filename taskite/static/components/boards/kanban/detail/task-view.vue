<script setup>
import { onMounted, ref } from 'vue';
import {
    Select,
    SelectOption,
    Tag,
    Skeleton,
    Avatar,
} from 'ant-design-vue';
import { handleResponseError, generateAvatar } from '@/utils/helpers';
import { taskDetailAPI, taskUpdateAPI } from '@/utils/api';
import { useKanbanStore } from '@/stores/kanban';
import TaskCommentList from './task-comment-list.vue';
import SubTasks from './sub-tasks.vue';
import { taskCommentsAPI, taskCommentsLastAPI } from '@/utils/api';

const store = useKanbanStore()

const props = defineProps(['board', 'workspace', 'taskId']);


const updateTask = async (updatedData) => {
    try {
        const { data } = await taskUpdateAPI(props.board.id, props.taskId, updatedData)
        store.updateTask(data)
        task.value = data

        const lastCommentRespone = await taskCommentsLastAPI(props.board.id, props.taskId)
        comments.value.push(lastCommentRespone.data)

        return data
    } catch (error) {
        handleResponseError(error)
    }
}

const task = ref(null)
const loadTask = async () => {
    try {
        const { data } = await taskDetailAPI(props.board.id, props.taskId)
        task.value = {
            ...data,
            oldStateId: data.stateId
        }
    } catch (error) {
        handleResponseError(error)
    }
}

const getAvatarSrc = (memberId) => {
    const member = store.members.find(m => m.id === memberId);
    return member ? (member.avatar || generateAvatar(member.firstName)) : '';
};

const updateState = async (stateId) => {
    // Update the task
    try {
        const { data } = await taskUpdateAPI(props.board.id, props.taskId, { stateId })
        store.updateTaskState(task.value.oldStateId, data)
        task.value = {
            ...data,
            oldStateId: data.stateId
        }

        const lastCommentRespone = await taskCommentsLastAPI(props.board.id, props.taskId)
        comments.value.push(lastCommentRespone.data)
    } catch (error) {
        handleResponseError(error)
    }
}

const comments = ref([])
const loadComments = async () => {
    try {
        const { data } = await taskCommentsAPI(props.board.id, props.taskId)
        comments.value = data.map((comment) => {
            return {
                ...comment,
                key: comment.id
            }
        })
    } catch (error) {
        handleResponseError(error)
    }
}

onMounted(() => {
    loadTask()
    loadComments()
})
</script>

<template>
    <div v-if="!!task">
        <div class="mb-4">
            <div class="flex gap-1">
                <Tag v-for="label in task.labels" :key="label.id" :bordered="false" :color="label.color">
                    {{ label.name }}
                </Tag>
            </div>
            <div class="text-2xl font-semibold">{{ task.summary }}</div>
            <div class="text-sm text-gray-500">
                <div class="flex items-center gap-1">
                    <div>Created by</div>
                    <Avatar :size="16"
                        :src="!!task.createdBy.avatar ? task.createdBy.avatar : generateAvatar(task.createdBy.firstName)" />
                    <div>{{ task.createdBy.firstName }} {{ task.createdBy?.lastName }}</div>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-12 items-center gap-2 mb-4">
            <div class="col-span-3">
                <div>Assignees</div>
            </div>
            <div class="col-span-9">
                <Select v-model:value="task.assigneeIds" mode="multiple" optionFilterProp="label"
                    @change="(assignees) => updateTask({ assignees })" class="w-full">

                    <template #tagRender="{ value }">
                        <Avatar size="small" :src="getAvatarSrc(value)" />
                    </template>


                    <SelectOption v-for="member in store.members" :key="member.id" :label="member.firstName">
                        <div class="flex items-center gap-2">
                            <Avatar size="small"
                                :src="!!member.avatar ? member.avatar : generateAvatar(member.firstName)" />
                            <div>{{ member.firstName }} {{ member?.lastName }}</div>
                        </div>
                    </SelectOption>
                </Select>
            </div>

            <div class="col-span-3">Issue type</div>
            <div class="col-span-9">
                <Select v-model:value="task.taskType" class="w-full" @change="(taskType) => updateTask({ taskType })">
                    <SelectOption value="issue">
                        Issue
                    </SelectOption>
                    <SelectOption value="bug">
                        Bug
                    </SelectOption>
                    <SelectOption value="story">
                        Story
                    </SelectOption>
                    <SelectOption value="feature">
                        Feature
                    </SelectOption>
                </Select>
            </div>

            <div class="col-span-3">Status</div>
            <div class="col-span-9">
                <Select v-model:value="task.stateId" class="w-full mb-2" @change="updateState">
                    <SelectOption :value="state.id" v-for="state in store.states" :key="state.id">
                        {{ state.name }}
                    </SelectOption>
                </Select>
            </div>

            <div class="col-span-3">Priority</div>
            <div class="col-span-9">
                <Select v-model:value="task.priorityId" @change="(priorityId) => updateTask({ priorityId })"
                    class="w-full">
                    <SelectOption :value="null">None</SelectOption>
                    <SelectOption :value="priority.id" v-for="priority in store.priorities" :key="priority.id">
                        {{ priority.name }}
                    </SelectOption>
                </Select>
            </div>
        </div>

        <div class="col-span-8 mb-4">
            <div class="text-lg font-semibold">Description</div>
            <div>
                {{ task.description }}
            </div>
        </div>

        <div class="mb-4">
            <SubTasks :boardId="props.board.id" :taskId="task.id" />
        </div>

        <div class="mb-6">
            <TaskCommentList :boardId="props.board.id" :taskId="props.taskId" :comments="comments" />
        </div>
    </div>
    <div v-else>
        <Skeleton />
    </div>
</template>



<style scoped></style>