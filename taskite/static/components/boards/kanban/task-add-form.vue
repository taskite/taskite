<script setup>
import { CloseOutlined, PlusOutlined } from '@ant-design/icons-vue';
import { Avatar, Button, Card, Dropdown, Form, FormItem, Input, Select, SelectOption, Textarea } from 'ant-design-vue';
import { h, onMounted, ref } from 'vue';
import { useKanbanStore } from '@/stores/kanban';
import { generateAvatar, handleResponseError, notify } from '@/utils/helpers';
import { taskCreateAPI } from '@/utils/api';

const props = defineProps(['board'])
const emit = defineEmits(['created'])

const store = useKanbanStore()

const taskAddForm = ref({
    summary: '',
    description: '',
    stateId: store.states.length > 0 ? store.states[0].id : '',
    assignees: [],
    priorityId: null,
    taskType: 'issue'
})
const formRef = ref();

const resetFields = () => {
    formRef.value.resetFields()
}

const submitForm = async (values) => {
    try {
        const { data } = await taskCreateAPI(props.board.id, values)
        resetFields()
        notify('CREATED', data.detail)
        emit('created', data.task)
    } catch (error) {
        handleResponseError(error)
    }
}
</script>

<template>
    <Card class="w-[26rem]" size="small">
        <div class="font-semibold text-lg border-b-1 border-gray-500">{{ props.board.name }}</div>
        <Form layout="vertical" :model="taskAddForm" hide-required-mark ref="formRef" @finish="submitForm">
            <div class="grid grid-cols-2 gap-2">
                <FormItem name="taskType" label="Task type">
                    <Select v-model:value="taskAddForm.taskType">
                        <SelectOption value="issue">Issue</SelectOption>
                        <SelectOption value="feature">Feature</SelectOption>
                        <SelectOption value="story">Story</SelectOption>
                        <SelectOption value="bug">Bug</SelectOption>
                    </Select>
                </FormItem>

                <FormItem name="stateId" label="State">
                    <Select v-model:value="taskAddForm.stateId">
                        <SelectOption :value="state.id" v-for="state in store.states" :key="state.id">{{ state.name }}
                        </SelectOption>
                    </Select>
                </FormItem>
            </div>

            <FormItem name="summary" label="Summary">
                <Input v-model:value="taskAddForm.summary" />
            </FormItem>

            <FormItem name="description" label="Description">
                <Textarea v-model:value="taskAddForm.description" :rows="4" />
            </FormItem>

            <FormItem name="priorityId" label="Priority">
                <Select v-model:value="taskAddForm.priorityId">
                    <SelectOption :value="null">None</SelectOption>
                    <SelectOption :value="priority.id" v-for="priority in store.priorities" :key="priority.id">
                        {{ priority.name }}
                    </SelectOption>
                </Select>
            </FormItem>

            <FormItem name="assignees" label="Assignees">
                <Select v-model:value="taskAddForm.assignees" mode="multiple" optionFilterProp="label">
                    <SelectOption v-for="member in store.members" :key="member.id" :label="member.firstName">
                        <div class="flex items-center gap-2">
                            <Avatar size="small"
                                :src="!!member.avatar ? member.avatar : generateAvatar(member.firstName)" />
                            <div>{{ member.firstName }} {{ member?.lastName }}</div>
                        </div>
                    </SelectOption>
                </Select>
            </FormItem>

            <div class="flex justify-end">
                <div class="flex gap-2">
                    <Button :icon="h(CloseOutlined)" @click="resetFields">Clear fields</Button>
                    <Button type="primary" html-type="submit" :icon="h(PlusOutlined)">Create</Button>
                </div>
            </div>
        </Form>
    </Card>
</template>