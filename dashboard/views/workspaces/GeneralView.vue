<script setup>
import { SaveOutlined } from '@ant-design/icons-vue';
import { h, ref } from 'vue'

const props = defineProps(['workspace'])

const workspaceForm = ref({
    name: props.workspace.name,
    description: props.workspace.description
})
</script>

<template>
    <div class="flex justify-center">
        <a-form layout="vertical" class="w-96">
            <a-form-item label="Name" :name="name">
                <a-input v-model:value="workspaceForm.name"></a-input>
            </a-form-item>

            <a-form-item label="Description" :name="description">
                <a-textarea v-model:value="workspaceForm.description" :rows="4"></a-textarea>
            </a-form-item>

            <a-form-item>
                <div class="flex justify-end gap-3">
                    <a-button>Cancel</a-button>
                    <a-button html-type="submit" type="primary" :icon="h(SaveOutlined)">Save</a-button>
                </div>
            </a-form-item>
        </a-form>
    </div>
        
</template>