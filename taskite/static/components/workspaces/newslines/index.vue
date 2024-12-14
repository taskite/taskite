<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import { PlusOutlined } from '@ant-design/icons-vue';
import { Button } from 'ant-design-vue';
import { h, onMounted, ref } from 'vue';
import { newslineListAPI } from '../../../utils/api/newslines';
import { handleResponseError } from '../../../utils/helpers';
const props = defineProps(['workspace', 'currentUser'])

const newslines = ref([])

const loadNewslines = async () => {
    try {
        const { data } = await newslineListAPI(props.workspace.id)
        newslines.value = data
    } catch (error) {
        handleResponseError(error)
    }
}

onMounted(() => {
    loadNewslines()
})
</script>

<template>
    <WorkspaceLayout :workspace="props.workspace" :currentUser="props.currentUser" page="newslines">
        <div class="p-4">
            <div class="flex justify-between items-center">
                <div class="text-2xl font-semibold mb-3">Newslines</div>
                <Button class="" type="primary" :icon="h(PlusOutlined)">Create newsline</Button>
            </div>
        </div>
    </WorkspaceLayout>
</template>
