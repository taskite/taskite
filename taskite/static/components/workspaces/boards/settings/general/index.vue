<script setup>
import BoardSettingsLayout from '@/components/base/board-settings-layout.vue';

const props = defineProps(['workspace', 'board'])
</script>

<template>
    <BoardSettingsLayout :workspace="props.workspace" :board="props.board" page="general">
        <h1>General setting</h1>
    </BoardSettingsLayout>
</template>