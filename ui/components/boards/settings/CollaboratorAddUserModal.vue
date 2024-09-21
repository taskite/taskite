<script setup>
import { useBoardStore } from '@/stores/board';
import { workspaceMembersSearchAPI } from '@/utils/api';
import { ref } from 'vue';
const searchValue = ref('')

const boardStore = useBoardStore()

const onSearch = async (value) => {
    try {
        await workspaceMembersSearchAPI(boardStore.selectedBoard.workspaceId, value)
    } catch (error) {
        console.log(error)
    }
}
</script>

<template>
  <div class="mb-1">Search by username, fullname or email</div>
  <a-input-search
    v-model:value="searchValue"
    @search="onSearch"
    class="w-full"
  />
</template>
