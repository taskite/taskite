<script setup>
import WorkspaceSettingsLayout from '@/components/base/workspace-settings-layout.vue';

const props = defineProps(['workspace', 'currentUser'])
</script>

<template>
    <WorkspaceSettingsLayout :workspace="props.workspace" :currentUser="props.currentUser" page="billing">
        <h1>Billing</h1>
    </WorkspaceSettingsLayout>
</template>