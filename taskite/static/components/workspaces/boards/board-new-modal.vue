<script setup>
import { PlusOutlined } from '@ant-design/icons-vue'
import {
  Form,
  FormItem,
  Input,
  Textarea,
  Button,
  message,
  Select,
  SelectOption,
} from 'ant-design-vue'
import { h, onMounted, ref } from 'vue'
import { boardCreateAPI, boardTemplatesAPI } from '@/utils/api'
import { handleResponseError } from '@/utils/helpers'

const props = defineProps(['workspace'])

const boardForm = ref({
  name: '',
  description: '',
  templateId: '',
})

const onSubmit = async (values) => {
  try {
    const postData = {
      workspaceId: props.workspace.id,
      ...values,
    }

    const { data } = await boardCreateAPI(postData)

    window.location.href = `/b/${data.slug}`
  } catch (error) {
    handleResponseError(error)
  }
}

const boardTemplates = ref([])
const fetchBoardTemplates = async () => {
  try {
    const { data } = await boardTemplatesAPI(props.workspace.id)
    boardTemplates.value = data.results
  } catch (error) {
    handleResponseError(error)
  }
}

onMounted(async () => {
  await fetchBoardTemplates()
})
</script>

<template>
  <div>
    <Form
      name="add-form"
      :model="boardForm"
      layout="vertical"
      @finish="onSubmit"
      hideRequiredMark
    >
      <FormItem
        label="Name"
        name="name"
        :rules="[{ required: true, message: 'Please enter board name' }]"
      >
        <Input v-model:value="boardForm.name" />
      </FormItem>

      <FormItem label="Description" name="description">
        <Textarea v-model:value="boardForm.description" :rows="5" />
      </FormItem>

      <FormItem label="Template" name="templateId">
        <Select v-model:value="boardForm.templateId">
          <SelectOption :value="null">No template</SelectOption>
          <SelectOption
            :value="template.id"
            v-for="template in boardTemplates"
            :key="template.id"
          >
            <div class="flex flex-col gap-1">
              <div class="font-semibold">{{ template.name }}</div>
              <div class="text-xs text-wrap">{{ template.description }}</div>
            </div>
          </SelectOption>
        </Select>
      </FormItem>

      <FormItem>
        <Button type="primary" :icon="h(PlusOutlined)" html-type="submit"
          >Create</Button
        >
      </FormItem>
    </Form>
  </div>
</template>
