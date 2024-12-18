<script setup>
import { Checkbox, CheckboxGroup, Tag } from 'ant-design-vue'
import { useKanbanStore } from '@/stores/kanban'
import { SyncOutlined } from '@ant-design/icons-vue'

const store = useKanbanStore()
</script>

<template>
  <CheckboxGroup v-model:value="store.sprintFilters" class="">
    <div class="flex flex-col gap-1">
      <div
        class="flex items-center gap-2"
        v-for="sprint in store.sprints"
        :key="sprint.id"
      >
        <Checkbox :value="sprint.id"></Checkbox>
        <div>
          <SyncOutlined class="text-xs" />
          <span class="ml-1">{{ sprint.name }}</span>
          <Tag
            v-if="!!store.activeSprint && store?.activeSprint.id === sprint.id"
            :bordered="false"
            size="small"
            class="ml-1 text-xs font-semibold text-primary"
            >Active</Tag
          >
        </div>
      </div>
    </div>
  </CheckboxGroup>
</template>
