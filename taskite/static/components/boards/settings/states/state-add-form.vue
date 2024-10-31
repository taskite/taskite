<script setup>
import { PlusOutlined } from '@ant-design/icons-vue';
import { Button, Card, Form, FormItem, Input, Textarea } from 'ant-design-vue';
import { h, ref } from 'vue';
import { handleResponseError } from '../../../../utils/helpers';
import { stateCreateAPI } from '../../../../utils/api';

const props = defineProps(['boardId'])
const emit = defineEmits(['added'])

const stateAddForm = ref({
    name: '',
    description: '',
})
const formRef = ref()


const onFinish = async (values) => {
    try {
        const { data } = await stateCreateAPI(props.boardId, values)
        emit('added', data)
        formRef.value.resetFields()
    } catch (error) {
        console.log(error)
        handleResponseError(error)
    }
}
</script>

<template>
    <Card size="small" class="w-80" title="Create state">
        <Form layout="vertical" :model="stateAddForm" name="state add form" @finish="onFinish" ref="formRef">
            <FormItem label="Name" name="name">
                <Input v-model:value="stateAddForm.name" />
            </FormItem>

            <FormItem label="Description" name="description">
                <Textarea v-model:value="stateAddForm.description" :rows="3" />
            </FormItem>

            <FormItem>
                <Button :icon="h(PlusOutlined)" html-type="submit">Add</Button>
            </FormItem>
        </Form>
    </Card>
</template>