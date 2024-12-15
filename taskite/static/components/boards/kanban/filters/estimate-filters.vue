<script setup>
import { Checkbox, CheckboxGroup } from 'ant-design-vue'
import { useKanbanStore } from '@/stores/kanban'

const store = useKanbanStore()
</script>

<template>
  <CheckboxGroup v-model:value="store.estimateFilters" class="">
    <div class="flex flex-col gap-1">
      <div
        class="flex items-center gap-2"
        v-for="estimate in store.estimates"
        :key="estimate.id"
      >
        <Checkbox :value="estimate.id"></Checkbox>
        <div>{{ estimate.value }}</div>
      </div>
    </div>
  </CheckboxGroup>
</template>
