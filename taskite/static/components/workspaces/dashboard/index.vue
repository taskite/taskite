<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue';

const props = defineProps(['workspace', 'currentUser'])
</script>

<template>
    <WorkspaceLayout :workspace="props.workspace" page="dashboard" :currentUser="props.currentUser">
        <div class="p-4">
            <div class="font-semibold text-2xl">Dashboard</div>
        </div>
    </WorkspaceLayout>
</template>

<style scoped>
</style>