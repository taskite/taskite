<script setup>
import WorkspaceSettingsLayout from '@/components/base/workspace-settings-layout.vue';
import { CloseOutlined, DeleteOutlined, LogoutOutlined, PlusOutlined } from '@ant-design/icons-vue';
import { Form, FormItem, Input, Textarea, Button, Divider, Collapse, CollapsePanel, Modal, Upload, Avatar, message } from 'ant-design-vue';
import { computed, h, ref } from 'vue';
import LeaveConfirmationModal from '@/components/workspaces/settings/general/leave-confirmation-modal.vue';
import DeleteConfirmationModal from '@/components/workspaces/settings/general/delete-confirmation-modal.vue';
import { workspaceUpdateAPI } from '@/utils/api';
import { uploadRequestHandler } from '@/utils/helpers';
import { generateAvatar, handleResponseError } from '@/utils/helpers';

const props = defineProps(['workspace', 'currentUser', 'membershipRole'])
const activeKey = ref([''])

const updateForm = ref({
    name: props.workspace.name,
    description: props.workspace.description,
    logo: props.workspace.logo,
    logoSrc: props.workspace.logoSrc
})

const onSubmit = async (values) => {
    try {
        await workspaceUpdateAPI(props.workspace.id, values)
        message.success('Updated workspace profile successfully!')
    } catch (error) {
        handleResponseError(error)
    }
}

const isAdmin = computed(() => {
    return props.membershipRole === 'admin'
})

const openLeaveConfirmationModal = ref(false)
const showLeaveConfirmationModal = () => {
    openLeaveConfirmationModal.value = true
}

const openDeleteConfirmationModal = ref(false)
const showDeleteConfirmationModal = () => {
    openDeleteConfirmationModal.value = true
}

const handleLogoUpload = async (options) => {
    const { fileKey, fileSrc } = await uploadRequestHandler(options)
    updateForm.value.logo = fileKey
    updateForm.value.logoSrc = fileSrc
}
const removeLogo = () => {
    updateForm.value.logo = null
    updateForm.value.logoSrc = null
}

</script>

<template>
    <WorkspaceSettingsLayout :workspace="props.workspace" :currentUser="props.currentUser" page="general">
        <div class="grid grid-cols-2 px-5 mt-3">
            <div class="font-semibold">General Setting</div>
            <div>
                <Form name="updateForm" :model="updateForm" layout="vertical" @finish="onSubmit" :disabled="!isAdmin">
                    <FormItem name="logo">
                        <div class="flex flex-col items-start gap-2">
                            <Upload :multiple="false" name="file" :customRequest="handleLogoUpload"
                                :show-upload-list="false">
                                <Avatar shape="square" :size="80"
                                    :src="!!updateForm.logoSrc ? updateForm.logoSrc : generateAvatar(props.workspace.name, 5)">
                                    <template #icon>
                                        <PlusOutlined />
                                    </template>
                                </Avatar>
                            </Upload>
                            <div class="flex items-center space-x-2 cursor-pointer text-xs" @click="removeLogo"
                                v-if="!!updateForm.logoSrc">
                                <CloseOutlined />
                                <span>Remove</span>
                            </div>
                        </div>
                    </FormItem>

                    <FormItem label="Workspace name" name="name">
                        <Input v-model:value="updateForm.name" />
                    </FormItem>

                    <FormItem label="Workspace description" name="description">
                        <Textarea v-model:value="updateForm.description" :rows="5" />
                    </FormItem>

                    <div class="flex justify-end">
                        <Button type="primary" html-type="submit">Update workspace</Button>
                    </div>
                </Form>
            </div>

        </div>
        <Divider />
        <div>
            <div class="font-semibold px-5 mb-5">Advance settings</div>
            <Collapse v-model:activeKey="activeKey" ghost>
                <CollapsePanel key="leave" header="Leave workspace">
                    <div class="text-gray-500">Please proceed with caution. Leaving this workspace will result in the
                        loss of access to all
                        associated data, projects, and pages. If you wish to rejoin in the future, you will need to be
                        re-invited by an existing member. Ensure you are certain of this decision before proceeding.
                    </div>
                    <Button danger class="mt-2" :icon="h(LogoutOutlined)" @click="showLeaveConfirmationModal">Leave
                        workspace</Button>
                </CollapsePanel>

                <CollapsePanel key="delete" header="Delete workspace" :collapsible="isAdmin ? 'header' : 'disabled'">
                    <div class="text-gray-500">Please proceed with extreme caution. Deleting this workspace will
                        permanently erase all
                        associated data, boards, and pages. Members will lose access immediately, and the workspace
                        cannot be recovered. If you are certain of this decision, please confirm before proceeding.
                    </div>
                    <Button danger class="mt-2" :icon="h(DeleteOutlined)" type="primary"
                        @click="showDeleteConfirmationModal">Delete workspace</Button>
                </CollapsePanel>
            </Collapse>
        </div>
    </WorkspaceSettingsLayout>

    <Modal v-model:open="openLeaveConfirmationModal" title="Leave confirmation" centered>
        <LeaveConfirmationModal :workspaceSlug="props.workspace.slug" />

        <template #footer>
            <!-- <Button @click="openLeaveConfirmationModal = false">Cancel</Button> -->
        </template>
    </Modal>

    <Modal v-model:open="openDeleteConfirmationModal" title="Delete confirmation" centered>
        <DeleteConfirmationModal :workspaceSlug="props.workspace.slug" />

        <template #footer>
            <!-- <Button @click="openLeaveConfirmationModal = false">Cancel</Button> -->
        </template>
    </Modal>
</template>