<script setup>
import BoardSettingsLayout from '@/components/base/board-settings-layout.vue';
import WorkspaceLayout from '@/components/base/workspace-layout.vue';
import { onMounted, ref, h } from 'vue';
import { stateListAPI } from '@/utils/api';
import { handleResponseError } from '@/utils/helpers';
import { CloseOutlined, DeleteOutlined, EditOutlined, HolderOutlined, PlusOutlined } from '@ant-design/icons-vue';
import { Button } from 'ant-design-vue';

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


onMounted(() => {
    loadStates()
})
</script>

<template>
    <WorkspaceLayout :workspace="workspace" page="boards">
        <BoardSettingsLayout :workspace="props.workspace" :board="props.board" page="states">
            <div class="text-lg">States</div>
            <div class="flex flex-col gap-3">
                <div v-for="state in states" class="w-full rounded overflow-hidden shadow-lg bg-white py-3 px-2">
                    <div class="flex justify-between relative group">
                        <div class="flex items-center gap-1 cursor-pointer">
                            <HolderOutlined />
                            <Button>{{ state.name }}</Button>
                        </div>
                        <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                            <Button type="text" :icon="h(EditOutlined)">Edit</Button>
                            <Button type="text" :icon="h(CloseOutlined)" danger></Button>
                        </div>
                    </div>
                </div>
                <div class="flex justify-center">
                    <Button :icon="h(PlusOutlined)" type="text" class="w-full mt-2">New state</Button>
                </div>
            </div>
        </BoardSettingsLayout>
    </WorkspaceLayout>
</template>