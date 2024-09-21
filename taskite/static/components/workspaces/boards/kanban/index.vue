<script setup>
import BoardLayout from '@/components/base/board-layout.vue';
import { useKanbanStore } from '@/stores/kanban';
import { onMounted } from 'vue';
import { taskListAPI, stateListAPI } from '@/utils/api';
import { Card } from 'ant-design-vue';
import { VueDraggable } from 'vue-draggable-plus';
import TaskCard from '@/components/workspaces/boards/kanban/task-card.vue';

const props = defineProps(['workspace', 'board'])
const store = useKanbanStore()

const fetchStates = async () => {
    try {
        const { data } = await stateListAPI(props.board.id)
        store.setStates(data)
    } catch (error) {
        console.log(error)
    }
}

const fetchTasks = async () => {
    try {
        const { data } = await taskListAPI(props.board.id)
        store.setTasks(data)
    } catch (error) {
        console.log(error)
    }
}

const loadKanban = async () => {
    try {
        await fetchStates()
        await fetchTasks()
        await store.setupKanban()
    } catch (error) {
        console.log(error)
    }
}

onMounted(() => {
    loadKanban()
})
</script>

<template>
    <BoardLayout :workspace="props.workspace" :board="props.board" page="kanban">
        <div class="h-screen flex flex-col">
            <!-- Header -->
            <div></div>

            <!-- Board -->
            <div class="flex gap-2 overflow-x-auto h-full px-3">
                <div class="w-80 flex-shrink-0" v-for="state in store.kanban" :key="state.id">
                    <div class="font-semi-bold text-lg my-1">{{ state.name }}</div>
                    <VueDraggable class="flex flex-col gap-2 overflow-y-auto state-tasks" v-model="state.tasks" group="states">
                        <div class="w-full" v-for="task in state.tasks" :key="task.id">
                            <TaskCard :board="props.board.id" :task="task" />
                        </div>
                    </VueDraggable>
                </div>
            </div>
        </div>
    </BoardLayout>
</template>

<style scoped>
.state-tasks {
  max-height: calc(100% - 7.5rem);
}

/* Custom scrollbar for the draggable container */
.state-tasks::-webkit-scrollbar {
  width: thin; /* Width of the scrollbar */
}

.state-tasks::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.5); /* Scrollbar color */
  border-radius: 4px; /* Rounded corners */
}

.state-tasks::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.1); /* Background track color */
}
</style>