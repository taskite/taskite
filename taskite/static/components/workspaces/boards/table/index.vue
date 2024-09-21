<script setup>
import BoardLayout from '@/components/base/board-layout.vue';

const props = defineProps(['workspace', 'board'])
</script>

<template>
    <BoardLayout :workspace="props.workspace" :board="props.board" page="table">
        <h1>Table</h1>
    </BoardLayout>
</template>
