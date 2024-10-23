<script setup>
import { Button, Input } from 'ant-design-vue';
import { computed, ref } from 'vue';
const props = defineProps(['workspaceSlug'])

const confirmName = ref('')

const disabled = computed(() => {
    return `workspaces/${props.workspaceSlug}` !== confirmName.value
})

const deleteWorkspace = () => {
    window.location.href = `/${props.workspaceSlug}/delete/`
}
</script>

<template>
    <div class="mb-2">Are you sure you want to delete this workspace? Deleting will clear all its boards,
        tasks, and
        resources data.</div>
    <div class="text-xs text-gray-400 mb-3">Note: This action is irreversible</div>

    <div class="mb-7">
        <div class="mb-1">Please type <span class="font-bold">workspaces/{{ props.workspaceSlug }}</span> to confirm.
        </div>
        <Input v-model:value="confirmName" />
    </div>

    <Button danger class="w-full" :disabled="disabled" @click="deleteWorkspace">I want to delete this workspace</Button>
</template>