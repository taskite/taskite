<script setup>
import {
  Card,
  Form,
  FormItem,
  Textarea,
  Button,
  Input,
  RangePicker,
  Checkbox,
} from 'ant-design-vue'
import { h, ref } from 'vue'
import { handleResponseError, notify } from '@/utils/helpers'
import { CloseOutlined, PlusOutlined } from '@ant-design/icons-vue'
import { sprintCreateAPI } from '@/utils/api'

const props = defineProps(['boardId'])
const emit = defineEmits(['created'])

const sprintAddForm = ref({
  name: '',
  description: '',
  range: [],
  isActive: false,
})
const formRef = ref(null)

const onSubmit = async (values) => {
  const postData = {
    ...values,
    startDate: values.range[0].format('YYYY-MM-DD'),
    endDate: values.range[1].format('YYYY-MM-DD'),
  }
  delete postData.range

  try {
    const { data } = await sprintCreateAPI(props.boardId, postData)
    notify('SUCCESS', data.detail)
    emit('created', data.sprint)
  } catch (error) {
    handleResponseError(error)
  } finally {
    formRef.value.resetFields()
  }
}
</script>

<template>
  <Card class="w-[26rem]" size="small">
    <Form
      :model="sprintAddForm"
      layout="vertical"
      @finish="onSubmit"
      ref="formRef"
    >
      <div class="grid grid-cols-5 gap-2">
        <FormItem label="Sprint name" name="name" class="col-span-2">
          <Input v-model:value="sprintAddForm.name" />
        </FormItem>
        <FormItem label="Date range" class="col-span-3" name="range">
          <RangePicker v-model:value="sprintAddForm.range" />
        </FormItem>
      </div>
      <FormItem label="Description" name="description">
        <Textarea v-model:value="sprintAddForm.description" :rows="4" />
      </FormItem>
      <FormItem name="isActive">
        <Checkbox v-model:checked="sprintAddForm.isActive"
          >Make this sprint active</Checkbox
        >
      </FormItem>
      <div class="flex justify-end gap-2">
        <Button @click="() => formRef.resetFields()" :icon="h(CloseOutlined)"
          >Clear Fields</Button
        >
        <Button type="primary" html-type="submit" :icon="h(PlusOutlined)"
          >Add</Button
        >
      </div>
    </Form>
  </Card>
</template>
