<script setup>
import BoardLayout from '@/components/base/board-layout.vue';
import WorkspaceLayout from '@/components/base/workspace-layout.vue';
const props = defineProps(['workspace', 'board'])
</script>

<template>
    <WorkspaceLayout :workspace="props.workspace" page="boards">
        <template #default>
            <BoardLayout :workspace="props.workspace" :board="props.board" page="table">
                <h1>Table</h1>
            </BoardLayout>
        </template>
    </WorkspaceLayout>
</template>
