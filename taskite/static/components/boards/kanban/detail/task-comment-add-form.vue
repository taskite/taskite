<script setup>
import { SaveOutlined } from '@ant-design/icons-vue'
import { Button, Form, FormItem, message, Textarea } from 'ant-design-vue'
import { h, ref } from 'vue'
import { handleResponseError } from '@/utils/helpers';
import { taskCommentsCreateAPI } from '@/utils/api';

const props = defineProps(['boardId', 'taskId'])
const emit = defineEmits(['added'])

const form = ref({
  content: '',
})
const formRef = ref()

const onFinish = async (values) => {
    try {
        const { data } = await taskCommentsCreateAPI(props.boardId, props.taskId, values)
        formRef.value.resetFields()

        emit('added', data)

        message.success('Comment added')
    } catch (error) {
        handleResponseError(error)
    }
}
</script>

<template>
  <Form
    layout="horizontal"
    :model="form"
    name="task-comment-add"
    @finish="onFinish"
    hide-required-mark
    ref="formRef"
  >
    <FormItem
      name="content"
      label="Comment"
      :rules="[{ message: 'Comment is requuired', required: true }]"
    >
      <Textarea v-model:value="form.content" :rows="2" class="w-full" />
    </FormItem>

    <div class="flex justify-end">
      <FormItem>
        <Button type="primary" html-type="submit" :icon="h(SaveOutlined)"
          >Comment</Button
        >
      </FormItem>
    </div>
  </Form>
</template>
