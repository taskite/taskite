<script setup>
import { onMounted, ref } from 'vue';

import WorkspaceLayout from '@/components/base/workspace-layout.vue';
import { boardListAPI } from '@/utils/api';
import { Card, Row, Col, Typography, message } from 'ant-design-vue';

const props = defineProps(['workspace', 'currentUser'])

const boards = ref([])
const error = ref('')
const fetchBoards = async () => {
    try {
        const { data } = await boardListAPI(props.workspace.id)
        boards.value = data
    } catch (err) {
        error.value = err.response?.data?.message || 'Failed to fetch boards.'
        message.error(error.value)
    }
}

const redirectToBoard = (board) => {
    window.location.href = `/${props.workspace.slug}/boards/${board.slug}/`
}

onMounted(() => {
    fetchBoards()
})
</script>

<template>
    <WorkspaceLayout :workspace="props.workspace" page="dashboard" :currentUser="props.currentUser">
        <Typography.Title :level="2">Boards</Typography.Title>
        <Row :gutter="16">
            <Col :span="8" v-for="board in boards" :key="board.id">
            <Card size="small" class="board-card" @click="redirectToBoard(board)">
                <Typography.Title :level="5">{{ board.name }}</Typography.Title>
            </Card>
            </Col>
        </Row>
    </WorkspaceLayout>
</template>

<style scoped>
.board-card {
    cursor: pointer;
}
</style>