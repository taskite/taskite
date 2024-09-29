<script setup>
import BoardSettingsLayout from '@/components/base/board-settings-layout.vue';
import { h, onMounted, ref } from 'vue';
import { Avatar, Form, FormItem, Input, Textarea, Upload, Button, message, Divider, Collapse, CollapsePanel } from 'ant-design-vue';
import { boardDetailAPI, boardUpdateAPI } from '@/utils/api';
import { CloseOutlined, DeleteOutlined, LogoutOutlined, PlusOutlined, SaveOutlined } from '@ant-design/icons-vue';
import { generateAvatar, uploadRequestHandler } from '@/utils/helpers';

const props = defineProps(['workspace', 'board', 'hasEditPermission'])
const activeKey = ref([''])

const boardForm = ref({
    name: '',
    description: '',
    cover: null,
    coverSrc: null,
    taskPrefix: '',
    slug: ''
})

const onFinish = async (values) => {
    try {
        await boardUpdateAPI(props.board.id, values)
        message.success('Board details updated successfully!')
    } catch (error) {
        console.log(error)
    }
}

const handleCoverUpload = async (options) => {
    const { fileKey, fileSrc } = await uploadRequestHandler(options)
    boardForm.value.cover = fileKey
    boardForm.value.coverSrc = fileSrc
}
const removeCover = () => {
    boardForm.value.cover = null
    boardForm.value.coverSrc = null
}

const fetchBoard = async () => {
    const { data } = await boardDetailAPI(props.board.id)
    boardForm.value = {
        name: data.name,
        description: data.description,
        cover: data.cover,
        coverSrc: data.coverSrc,
        taskPrefix: data.taskPrefix,
        slug: data.slug
    }
}

onMounted(() => {
    fetchBoard()
})
</script>

<template>
    <BoardSettingsLayout :workspace="props.workspace" :board="props.board" page="general">
        <div class="mx-auto px-4">
            <div class="max-w-3xl mx-auto">
                <Form :model="boardForm" layout="vertical" @finish="onFinish" :disabled="!props.hasEditPermission">
                    <FormItem name="cover">
                        <div class="flex flex-col items-start gap-2">
                            <Upload :multiple="false" name="file" :customRequest="handleCoverUpload"
                                :show-upload-list="false">
                                <Avatar shape="square" :size="80"
                                    :src="!!boardForm.cover ? boardForm.coverSrc : generateAvatar(board.name, 10)">
                                    <template #icon>
                                        <PlusOutlined />
                                    </template>
                                </Avatar>
                            </Upload>
                            <div class="flex items-center space-x-2 cursor-pointer text-xs" @click="removeCover"
                                v-if="!!boardForm.coverSrc">
                                <CloseOutlined />
                                <span>Remove</span>
                            </div>
                        </div>
                    </FormItem>

                    <div class="grid grid-cols-2 gap-4">
                        <FormItem label="Name" name="name">
                            <Input v-model:value="boardForm.name" />
                        </FormItem>

                        <FormItem label="Board ID" name="slug">
                            <Input v-model:value="boardForm.slug" />
                        </FormItem>
                    </div>

                    <FormItem label="Description" name="description">
                        <Textarea v-model:value="boardForm.description" :rows="4" />
                    </FormItem>

                    <div class="grid grid-cols-2 gap-4">
                        <FormItem label="Task prefix" name="taskPrefix">
                            <Input v-model:value="boardForm.taskPrefix" />
                        </FormItem>
                    </div>

                    <div class="flex justify-end">
                        <FormItem>
                            <Button type="primary" html-type="submit" :icon="h(SaveOutlined)">Update board</Button>
                        </FormItem>
                    </div>
                </Form>

                <Divider />
                <Collapse v-model:activeKey="activeKey" ghost>
                    <CollapsePanel key="leave" header="Leave board">
                        <div class="text-gray-500">Please proceed with caution. Leaving this board will result in the
                            loss of access to all
                            associated tasks. If you wish to rejoin in the future, you will need to be
                            added by an existing member. Ensure you are certain of this decision before proceeding.
                        </div>
                        <Button danger class="mt-2" :icon="h(LogoutOutlined)">Leave
                            board</Button>
                    </CollapsePanel>

                    <CollapsePanel key="delete" header="Delete board"
                        :collapsible="hasEditPermission ? 'header' : 'disabled'">
                        <div class="text-gray-500">Please proceed with extreme caution. Deleting this workspace will
                            permanently erase all
                            associated data, tasks. Members will lose access immediately, and the workspace
                            cannot be recovered. If you are certain of this decision, please confirm before proceeding.
                        </div>
                        <Button danger class="mt-2" :icon="h(DeleteOutlined)" type="primary">Delete board</Button>
                    </CollapsePanel>
                </Collapse>
            </div>
        </div>
    </BoardSettingsLayout>
</template>