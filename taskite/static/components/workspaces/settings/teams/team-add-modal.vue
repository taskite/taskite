<script setup>
import { PlusOutlined } from '@ant-design/icons-vue';
import { Form, FormItem, Input, Textarea, Button, message } from 'ant-design-vue';
import { h, ref } from 'vue';
import { workspaceTeamCreateAPI } from '@/utils/api';

const props = defineProps(['workspace'])
const emit = defineEmits(['teamAdded'])

const formRef = ref();
const addForm = ref({
    name: '',
    description: ''
})

const onSubmit = async (values) => {
    try {
        const { data } = await workspaceTeamCreateAPI(props.workspace.id, values)
        formRef.value.resetFields()
        emit('teamAdded', data)
    } catch (error) {
        console.log(error)
    }
}
</script>

<template>
    <Form name="addForm" :model="addForm" @finish="onSubmit" layout="vertical" ref="formRef" hide-required-mark>
        <FormItem label="Name" name="name" :rules="[{ required: true, message: 'Please enter team name' }]">
            <Input v-model:value="addForm.name" />
        </FormItem>

        <FormItem label="Description" name="description">
            <Textarea v-model:value="addForm.description" :rows="4" />
        </FormItem>

        <FormItem>
            <Button html-type="submit" type="primary" :icon="h(PlusOutlined)">Create</Button>
        </FormItem>
    </Form>
</template>