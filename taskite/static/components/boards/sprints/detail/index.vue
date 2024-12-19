<script setup>
const props = defineProps(['workspace', 'board', 'sprint'])

import KanbanBoard from '@/components/boards/kanban/index.vue'
</script>

<template>
  <KanbanBoard
    :board="props.board"
    :workspace="props.workspace"
    :currentSprint="props.sprint"
    currentTab="sprints"
  />
</template>
