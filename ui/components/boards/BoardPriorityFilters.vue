<script setup>
import { useBoardStore } from '@/stores/board'

const boardStore = useBoardStore()
</script>

<template>
  <div class="font-bold text-xs mb-1">Priorities</div>
  <a-checkbox-group v-model:value="boardStore.prioritiesFilter">
    <div class="flex flex-col gap-1">
      <a-checkbox
        v-for="priority in boardStore.priorities"
        :key="priority.id"
        :value="priority.id"
      >
        {{ priority.name }}
      </a-checkbox>
    </div>
  </a-checkbox-group>
</template>
