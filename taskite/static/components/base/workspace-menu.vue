<script setup>
import { Avatar, Button, Divider, Skeleton } from 'ant-design-vue';
import { h, onMounted, ref } from 'vue';
import { workspaceListAPI } from '@/utils/api';
import { handleResponseError, generateAvatar } from '@/utils/helpers';
import { PlusCircleOutlined } from '@ant-design/icons-vue';

const props = defineProps(['workspace'])

const activeWorkspace = ref([props.workspace.id])

const loading = ref(false)
const workspaces = ref([])
const fetchWorkspace = async () => {
    try {
        loading.value = true
        const { data } = await workspaceListAPI()
        workspaces.value = data
    } catch (error) {
        handleResponseError(error)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchWorkspace()
})

const redirectToWorkspace = (workspaceSlug) => {
    window.location.href = `/${workspaceSlug}`
}

const redirectToCreatePage = () => {
    window.location.href = `/create`
}
</script>

<template>
    <div class="p-3 w-80 rounded shadow-lg bg-white">
        <div class="text-sm font-semibold text-gray-500 mb-2">Workspaces</div>
        <Skeleton v-if="loading" class="p-2" />
        <div class="flex flex-col gap-2" v-else>
            <div v-for="workspace in workspaces" :key="workspace.id"
                class="flex gap-2 items-center cursor-pointer hover:bg-gray-100 p-1"
                :class="{ 'bg-gray-100': workspace.id === props.workspace.id }"
                @click="redirectToWorkspace(workspace.slug)">
                <Avatar :src="!!workspace.logo ? workspace.logoSrc : generateAvatar(workspace.name, 10)"
                    shape="square" />
                <div>{{ workspace.name }}</div>
            </div>
        </div>
        <Divider class="p-0 m-2" />
        <Button :icon="h(PlusCircleOutlined)" type="text" class="w-full" @click="redirectToCreatePage">Create new workspace</Button>
    </div>
</template>