<script setup>
import BoardSettingsLayout from '@/components/base/board-settings-layout.vue';
import WorkspaceLayout from '@/components/base/workspace-layout.vue';
import { onMounted, ref, h } from 'vue';
import { stateListAPI, stateSequenceUpdateAPI, stateDeleteAPI } from '@/utils/api';
import { handleResponseError } from '@/utils/helpers';
import { CloseOutlined, EditOutlined, HolderOutlined, PlusOutlined } from '@ant-design/icons-vue';
import { Button, FormItem, Input, Textarea, Modal, Dropdown, message } from 'ant-design-vue';
import { VueDraggable } from 'vue-draggable-plus';
import StateAddForm from './state-add-form.vue';

const props = defineProps(['workspace', 'board', 'hasEditPermission'])

const states = ref([])
const loadStates = async () => {
    try {
        const { data } = await stateListAPI(props.board.id)
        states.value = data
    } catch (error) {
        handleResponseError(error)
    }
}

const onUpdate = async (event) => {
    const updatedData = {}
    try {
        const state = states.value[event.newIndex]

        if (event.newIndex === 0 && states.value.length === 1) {
            // Empty
        }
        else if (event.newIndex === 0) {
            updatedData['nextState'] = states.value[event.newIndex + 1].id
        } else if (event.newIndex === states.value.length - 1) {
            updatedData['previousState'] = states.value[event.newIndex - 1].id
        } else {
            updatedData['nextState'] = states.value[event.newIndex + 1].id
            updatedData['previousState'] = states.value[event.newIndex - 1].id
        }

        const { data } = await stateSequenceUpdateAPI(props.board.id, state.id, updatedData)
        state.sequence = data.newSequence
    } catch (error) {
        handleResponseError(error)
    }
}

onMounted(() => {
    loadStates()
})

const showAddStateDropdown = ref(false)
const addState = (newState) => {
    states.value.push(newState)
    message.success(`New state ${newState.name} has been added.`)
    showAddStateDropdown.value = false
}

const deleteState = async (stateId) => {
    try {
        await stateDeleteAPI(props.board.id, stateId)
        states.value = states.value.filter(state => state.id !== stateId)
        message.success('State got deleted')
    } catch (error) {

    }
}
</script>

<template>
    <WorkspaceLayout :workspace="workspace" page="boards">
        <BoardSettingsLayout :workspace="props.workspace" :board="props.board" page="states">
            <div class="flex justify-between mb-2">
                <div class="text-lg">States</div>
                <div>
                    <Dropdown v-model:open="showAddStateDropdown" :trigger="['click']">
                        <Button type="primary" :icon="h(PlusOutlined)" :disabled="!props.hasEditPermission">Add
                            state</Button>

                        <template #overlay>
                            <StateAddForm :boardId="props.board.id" @added="addState" />
                        </template>
                    </Dropdown>
                </div>
            </div>
            <div class="flex flex-col gap-2">
                <VueDraggable v-model="states" class="flex flex-col gap-1" @update="onUpdate">
                    <div v-for="state in states" class="w-full rounded overflow-hidden shadow-lg bg-white py-3 px-2">
                        <div class="flex justify-between relative group">
                            <div class="flex items-center gap-1 cursor-pointer">
                                <HolderOutlined />
                                <Button>{{ state.name }}</Button>
                            </div>
                            <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                                <Button type="text" :icon="h(EditOutlined)"
                                    :disabled="!props.hasEditPermission">Edit</Button>
                                <Button type="text" :icon="h(CloseOutlined)" danger @click="deleteState(state.id)"
                                    :disabled="!props.hasEditPermission"></Button>
                            </div>
                        </div>
                    </div>
                </VueDraggable>
            </div>
        </BoardSettingsLayout>
    </WorkspaceLayout>
</template>