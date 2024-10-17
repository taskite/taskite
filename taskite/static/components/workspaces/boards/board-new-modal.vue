<script setup>
import { PlusOutlined } from '@ant-design/icons-vue';
import { Form, FormItem, Input, Textarea, Button, message } from 'ant-design-vue';
import { h, ref } from 'vue';
import { boardCreateAPI } from '@/utils/api';
import { handleResponseError } from '@/utils/helpers';

const props = defineProps(['workspace'])

const boardForm = ref({
    name: '',
    description: ''
})

const onSubmit = async (values) => {
    try {
        const postData = {
            workspaceId: props.workspace.id,
            ...values
        }

        const { data } = await boardCreateAPI(postData)

        window.location.href = `/b/${data.slug}`
    } catch (error) {
        handleResponseError(error)
    }
}
</script>

<template>
    <div>
        <Form name="add-form" :model="boardForm" layout="vertical" @finish="onSubmit" hideRequiredMark>
            <FormItem label="Name" name="name" :rules="[{ required: true, message: 'Please enter board name' }]">
                <Input v-model:value="boardForm.name" />
            </FormItem>

            <FormItem label="Description" name="description">
                <Textarea v-model:value="boardForm.description" :rows="5" />
            </FormItem>

            <FormItem>
                <Button type="primary" :icon="h(PlusOutlined)" html-type="submit">Create</Button>
            </FormItem>
        </Form>
    </div>
</template>