<script setup>
import BoardLayout from '@/components/base/board-layout.vue';
import { useKanbanStore } from '@/stores/kanban';
import { h, onMounted, ref, watch } from 'vue';
import { taskListAPI, stateListAPI, boardMembersListAPI, priorityListAPI, taskUpdateSequence, taskCreateAPI, labelListAPI } from '@/utils/api';
import { VueDraggable } from 'vue-draggable-plus';
import TaskCard from '@/components/boards/kanban/task-card.vue';
import { handleResponseError } from '@/utils/helpers';
import { Button, Dropdown, Card, Input, AvatarGroup, Avatar, Drawer, Breadcrumb, BreadcrumbItem } from 'ant-design-vue';
import { FilterOutlined, PlusOutlined, ReloadOutlined, UnorderedListOutlined } from '@ant-design/icons-vue';
import WorkspaceLayout from '@/components/base/workspace-layout.vue';
import FilterList from '@/components/boards/kanban/filters/filter-list.vue';
import TaskAddForm from '@/components/boards/kanban/task-add-form.vue';
import TaskView from '@/components/boards/kanban/detail/task-view.vue';
import { generateAvatar } from '@/utils/helpers';

const props = defineProps(['workspace', 'board'])
const store = useKanbanStore()

const fetchStates = async () => {
    try {
        const { data } = await stateListAPI(props.board.id)
        store.setStates(data)
    } catch (error) {
        handleResponseError(error)
    }
}

const fetchTasks = async (filters = {}) => {
    try {
        const { data } = await taskListAPI(props.board.id, filters)
        store.setTasks(data)
    } catch (error) {
        handleResponseError(error)
    }
}

const fetchMembers = async () => {
    try {
        const { data } = await boardMembersListAPI(props.board.id)
        store.setMembers(data)
    } catch (error) {
        handleResponseError(error)
    }
}

const fetchPriorities = async () => {
    try {
        const { data } = await priorityListAPI(props.board.id)
        store.setPriorities(data)
    } catch (error) {
        handleResponseError(error)
    }
}

const fetchLabels = async () => {
    try {
        const { data } = await labelListAPI(props.board.id)
        store.setLabels(data)
    } catch (error) {
        handleResponseError(error)
    }
}

const loadKanban = async () => {
    try {
        await fetchStates()
        await fetchTasks()
        await store.setupKanban()

        fetchMembers()
        fetchPriorities()
        fetchLabels()
    } catch (error) {
        handleResponseError(error)
    }
}

const updateTaskSequence = async (event, stateId) => {
    const updatedData = {
        stateId,
    }
    try {
        const state = store.kanban.find((state) => state.id === stateId)
        const task = state.tasks[event.newIndex]

        if (event.newIndex === 0 && state.tasks.length === 1) {
            // Empty
        }
        else if (event.newIndex === 0) {
            updatedData['nextTask'] = state.tasks[event.newIndex + 1].id
        } else if (event.newIndex === state.tasks.length - 1) {
            updatedData['previousTask'] = state.tasks[event.newIndex - 1].id
        } else {
            updatedData['nextTask'] = state.tasks[event.newIndex + 1].id
            updatedData['previousTask'] = state.tasks[event.newIndex - 1].id
        }

        const { data } = await taskUpdateSequence(props.board.id, task.id, updatedData)
        task.sequence = data.newSequence
        task.stateId = stateId
    } catch (error) {
        handleResponseError(error)
    }
}

const openAddTaskDropdown = ref(false)
const addTaskAndCloseAddTaskDropdown = (newTask) => {
    store.addNewTask(newTask)
    openAddTaskDropdown.value = false
}

onMounted(() => {
    loadKanban()
})

const openFilterDropdown = ref(false)

watch(() => [store.assigneeFilters, store.taskTypes, store.priorityFilters, store.labelFilters], async () => {
    await fetchTasks({ assignees: store.assigneeFilters, taskTypes: store.taskTypes, priorities: store.priorityFilters, labels: store.labelFilters })
    await store.setupKanban()
})

const activeTaskAddCard = ref('')
const activateAddCard = (stateId) => {
    activeTaskAddCard.value = stateId
}
const closeActiveTaskCard = () => {
    activeTaskAddCard.value = ''
}
const createNewTask = async (event, stateId) => {
    const newTaskData = {
        "summary": event.target.value,
        "stateId": stateId,
        "taskType": "issue",
        "assignees": []
    }

    try {
        const { data } = await taskCreateAPI(props.board.id, newTaskData)
        store.addNewTask(data)
        closeActiveTaskCard()
    } catch (error) {
        handleResponseError(error)
    }
}

const openTaskAddModal = ref(false)
const selectedTask = ref('')
const showTaskAddModal = (taskId) => {
    store.setSelectedTask(taskId)
    openTaskAddModal.value = true
}
const closeTaskAddModal = () => {
    store.setSelectedTask('')
    openTaskAddModal.value = false
}
</script>

<template>
    <div class="min-h-screen">
        <WorkspaceLayout :workspace="props.workspace" page="boards">
            <BoardLayout :workspace="props.workspace" :board="props.board" page="kanban">
                <template #default>
                    <div class="board-container">
                        <div class="flex space-x-1">
                            <div v-for="state in store.kanban" :key="state.id"
                                class="column p-1 rounded-lg w-80 flex-shrink-0">
                                <div class="font-semibold mb-2">{{ state.name }}</div>
                                <div class="task-list">
                                    <VueDraggable class="flex flex-col space-y-2" v-model="state.tasks" group="states"
                                        @update="(event) => updateTaskSequence(event, state.id)"
                                        @add="(event) => updateTaskSequence(event, state.id)">
                                        <div v-for="task in state.tasks" :key="task.id" class="cursor-pointer"
                                            @click="showTaskAddModal(task.id)">
                                            <Card size="small"
                                                class="rounded hover:border-1 hover:border-primary transition duration-300"
                                                :class="{ 'border-1 border-primary': store.selectedTask === task.id }">
                                                <TaskCard :task="task" :boardId="props.board.id" />
                                            </Card>
                                        </div>
                                    </VueDraggable>
                                </div>

                                <Card size="small mt-2" class="rounded" v-if="activeTaskAddCard === state.id">
                                    <Input :bordered="false" placeholder="Summary"
                                        @keyup.enter="(event) => createNewTask(event, state.id)" />
                                    <div class="flex justify-end">
                                        <Button type="text" size="small" @click="closeActiveTaskCard">Close</Button>
                                    </div>
                                </Card>

                                <div class="mt-2">
                                    <span class="text-sm" @click="activateAddCard(state.id)">+ Add Task</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>

                <template #actions>
                    <div class="flex me-2 gap-3 items-center">
                        <Button type="text" :icon="h(ReloadOutlined)">Refresh board</Button>
                        <Dropdown :trigger="['click']" placement="bottomRight">
                            <AvatarGroup size="small" :max-count="5">
                                <Avatar v-for="member in store.members" :key="member.id"
                                    :src="!!member.avatar ? member.avatar : generateAvatar(member.firstName)" />
                            </AvatarGroup>
                            <template #overlay>

                            </template>
                        </Dropdown>

                        <Button type="text" :icon="h(UnorderedListOutlined)">Group by</Button>

                        <Dropdown :trigger="['click']" v-model:open="openFilterDropdown" placement="bottomRight">
                            <Button :icon="h(FilterOutlined)">Filters</Button>
                            <template #overlay>
                                <FilterList />
                            </template>
                        </Dropdown>

                        <Dropdown :trigger="['click']" v-model:open="openAddTaskDropdown" placement="bottomRight">
                            <Button type="primary" :icon="h(PlusOutlined)">Add task</Button>
                            <template #overlay>
                                <TaskAddForm :board="props.board" @created="addTaskAndCloseAddTaskDropdown" />
                            </template>
                        </Dropdown>
                    </div>
                </template>
            </BoardLayout>

            <Drawer centered v-model:open="openTaskAddModal" destroyOnClose :width="920"
                :afterClose="closeTaskAddModal">
                <TaskView :board="props.board" :workspace="props.workspace" :taskId="store.selectedTask" />
                <template #extra>
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
                    </Breadcrumb>
                </template>
            </Drawer>
        </WorkspaceLayout>
    </div>
</template>

<style scoped>
.board-container {
    overflow-x: auto;
}

.task-list {
    min-height: 50px;
    max-height: calc(100vh - 115px);
    overflow-y: auto;
}

/* Custom scrollbar styles */
.task-list::-webkit-scrollbar {
    width: 8px;
}

.task-list::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.task-list::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}

.task-list::-webkit-scrollbar-thumb:hover {
    background: #555;
}

/* For Firefox */
.task-list {
    scrollbar-width: thin;
    scrollbar-color: #888 #f1f1f1;
}
</style>