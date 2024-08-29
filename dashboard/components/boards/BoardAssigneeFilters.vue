<script setup>
import { useBoardStore } from '@/stores/board'
import { generateAvatar } from '@/utils/generators'

const boardStore = useBoardStore()
</script>

<template>
  <div class="font-bold text-xs mb-1">Assignees</div>
  <a-checkbox-group v-model:value="boardStore.assigneesFilter">
    <div class="flex flex-col gap-1">
      <a-checkbox
        v-for="member in boardStore.members"
        :key="member.id"
        :value="member.id"
      >
        <span>
          <a-avatar
            size="small"
            :src="generateAvatar(member.firstName)"
          ></a-avatar>
          {{ member.firstName }} {{ member?.lastName }}
        </span>
      </a-checkbox>
    </div>
  </a-checkbox-group>
</template>
