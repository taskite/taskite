<script setup>
import { onMounted, ref } from 'vue';
import {
    Button,
    Breadcrumb,
    BreadcrumbItem,
    Select,
    SelectOption,
    Tag,
    Skeleton,
    Avatar,
    List,
    ListItem,
    Comment
} from 'ant-design-vue';
import {
    ShareAltOutlined,
} from '@ant-design/icons-vue';
import { handleResponseError, generateAvatar } from '@/utils/helpers';
import { taskDetailAPI, taskUpdateAPI, taskCommentsAPI } from '@/utils/api';
import { useKanbanStore } from '@/stores/kanban';

const store = useKanbanStore()

const props = defineProps(['board', 'workspace', 'taskId']);

const getTypeColor = (type) => {
    const colors = {
        bug: 'red',
        issue: 'blue',
        feature: 'green',
        story: 'brown'
    };
    return colors[type] || 'default';
};

const updateTask = async (updatedData) => {
    try {
        const { data } = await taskUpdateAPI(props.board.id, props.taskId, updatedData)
        store.updateTask(data)
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
            assigneeIds: data.assignees.map(assignee => assignee.id),
            oldStateId: data.stateId
        }
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
            assigneeIds: data.assignees.map(assignee => assignee.id),
            oldStateId: data.stateId
        }
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
    <div class="flex flex-col h-full" v-if="!!task">
        <!-- Header -->
        <div class="flex justify-between items-center mb-4 pb-2 border-b border-gray-200">
            <div class="flex items-center space-x-2 text-sm text-gray-500">
                <Breadcrumb>
                    <BreadcrumbItem>
                        <Avatar :size="20" shape="square"
                            :src="!!props.workspace.logo ? props.workspace.logoSrc : generateAvatar(props.workspace.name, 10)" />
                        <span class="ml-2">{{ props.workspace.name }}</span>
                    </BreadcrumbItem>
                    <BreadcrumbItem>
                        <Avatar :size="20" shape="square"
                            :src="!!props.board.cover ? props.board.cover : generateAvatar(props.board.name, 10)" />
                        <span class="ml-2">{{ props.board.name }}</span>
                    </BreadcrumbItem>
                    <BreadcrumbItem>{{ task.name }}</BreadcrumbItem>
                </Breadcrumb>
            </div>
            <div class="flex items-center space-x-2">
                <Button type="text">
                    <template #icon>
                        <ShareAltOutlined />
                    </template>
                    Share
                </Button>
            </div>
        </div>

        <!-- Content -->
        <div class="flex flex-grow overflow-hidden">
            <!-- Main Content -->
            <div class="flex-grow overflow-y-auto pr-4">
                <div class="mb-4">
                    <Tag :bordered="false" :color="getTypeColor(task.taskType)">{{ task.taskType }}</Tag>
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

                <div class="mb-6">
                    <div class="text-lg font-semibold">Description</div>
                    <div>
                        {{ task.description }}
                    </div>
                </div>

                <div class="mb-6">
                    <h3 class="text-lg font-semibold mb-2">Comments</h3>
                    <div v-for="comment in comments" :key="comment.id" class="mb-4 flex items-start space-x-3">
                        <Avatar :src="comment.author.avatar" :size="28" :alt="`${comment.author.firstName}'s avatar`" />
                        <div class="flex-grow">
                            <div class="flex items-center space-x-2 mb-1">
                                <span class="font-xs text-gray-450">{{ comment.author.firstName }}</span>
                                <span class="text-sm text-gray-800">{{ comment.time }}</span>
                            </div>
                            <p class="text-gray-600 mb-2">{{ comment.content }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Sidebar -->
            <div class="w-64 flex-shrink-0 border-l border-gray-200 pl-4">
                <div class="mb-4">
                    <div class="text-sm font-semibold mb-2">Status</div>
                    <Select v-model:value="task.stateId" class="w-52 mb-2" @change="updateState">
                        <SelectOption :value="state.id" v-for="state in store.states" :key="state.id">{{ state.name }}
                        </SelectOption>
                    </Select>
                </div>

                <div class="mb-4">
                    <div class="text-sm font-semibold mb-2">Assignees</div>
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

                <div class="mb-4">
                    <div class="text-sm font-semibold mb-2">Priority</div>
                    <Select v-model:value="task.priorityId" @change="(priorityId) => updateTask({ priorityId })"
                        class="w-full">
                        <SelectOption :value="null">None</SelectOption>
                        <SelectOption :value="priority.id" v-for="priority in store.priorities" :key="priority.id">
                            {{ priority.name }}
                        </SelectOption>
                    </Select>
                </div>

                <div class="mb-4">
                    <h3 class="text-sm font-semibold mb-2">Type</h3>
                    <Select v-model:value="task.taskType" class="w-full"
                        @change="(taskType) => updateTask({ taskType })">
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
            </div>
        </div>
    </div>
    <div v-else>
        <Skeleton />
    </div>
</template>



<style scoped></style>