<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue';
import { Card, Button, Modal } from 'ant-design-vue';
import { ref, onMounted, h } from 'vue';
import { boardListAPI } from '@/utils/api';
import dayjs from 'dayjs';
import { PlusOutlined } from '@ant-design/icons-vue';
import BoardNewModal from './board-new-modal.vue';
import { handleResponseError } from '@/utils/helpers';

const props = defineProps(['workspace', 'currentUser'])

const boards = ref([])
const fetchBoards = async () => {
    try {
        const { data } = await boardListAPI(props.workspace.id)
        boards.value = data
    } catch (err) {
        handleResponseError(err)
    } finally {
    }
}

const redirectToBoard = (board) => {
    window.location.href = `/b/${board.id}/`
}

const openNewBoardModal = ref(false)
const showNewBoardModal = () => {
    openNewBoardModal.value = true
}
const closeNewBoardModal = () => {
    openNewBoardModal.value = false
}

onMounted(() => {
    fetchBoards()
})
</script>

<template>
    <WorkspaceLayout :workspace="props.workspace" :currentUser="props.currentUser" page="boards">
        <div class="p-4">
            <div class="flex justify-between items-center">
                <div class="text-2xl font-semibold mb-3">Boards</div>
                <Button class="" type="primary" :icon="h(PlusOutlined)" @click="showNewBoardModal">New board</Button>
            </div>
            <div class="grid grid-cols-3 gap-3">
                <Card v-for="board in boards" :key="board.id" size="small" @click="redirectToBoard(board)"
                    class="cursor-pointer hover:border-solid hover:border-1 hover:border-primary">
                    <div class="font-semibold">{{ board.name }}</div>
                    <div class="text-xs">Created on {{ dayjs(board.createdAt).format('MMMM D, YYYY') }}</div>
                </Card>
            </div>
        </div>
        <Modal v-model:open="openNewBoardModal" title="New board">
            <template #footer>
                <Button @click="closeNewBoardModal">Cancel</Button>
            </template>
            <BoardNewModal :workspace="props.workspace"></BoardNewModal>
        </Modal>
    </WorkspaceLayout>
</template>