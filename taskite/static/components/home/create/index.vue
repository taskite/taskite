<script setup>
import BaseLayout from '@/components/base/base-layout.vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import { Button, Form, FormItem, Input, Textarea } from 'ant-design-vue';
import { h, ref } from 'vue';
import { workspaceCreareAPI } from '@/utils/api';
import { handleResponseError } from '@/utils/helpers';

const createForm = ref({
    name: '',
    description: ''
})

const onFinish = async (values) => {
    try {
        const { data } = await workspaceCreareAPI(values)
        window.location.href = `/${data.slug}/boards`
    } catch (error) {
        handleResponseError(error)
    }
}
</script>

<template>
    <BaseLayout>
        <div class="flex justify-center items-center h-screen bg-gray-100">
            <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
                <h2 class="text-2xl font-bold mb-6 text-center">Create Workspace</h2>
                <Form name="createForm" :model="createForm" layout="vertical" hide-required-mark @finish="onFinish">
                    <FormItem label="Name" name="name"
                        :rules="[{ required: true, message: 'Please enter workspace name!' }]">
                        <Input v-model:value="createForm.name" />
                    </FormItem>

                    <FormItem label="Description" name="description">
                        <Textarea v-model:value="createForm.description" :rows="4" />
                    </FormItem>
                    <div class="flex justify-end">
                        <FormItem>
                            <Button type="primary" html-type="submit" :icon="h(PlusOutlined)">Create workspace</Button>
                        </FormItem>
                    </div>
                </Form>
            </div>
        </div>
    </BaseLayout>
</template>