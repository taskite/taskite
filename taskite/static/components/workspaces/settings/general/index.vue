<script setup>
import WorkspaceSettingsLayout from '@/components/base/workspace-settings-layout.vue';
import { DeleteOutlined, LogoutOutlined } from '@ant-design/icons-vue';
import { Form, FormItem, Input, Textarea, Button, Divider, Collapse, CollapsePanel, Modal } from 'ant-design-vue';
import { computed, h, ref } from 'vue';
import LeaveConfirmationModal from '@/components/workspaces/settings/general/leave-confirmation-modal.vue';

const props = defineProps(['workspace', 'currentUser', 'membershipRole'])
const activeKey = ref([''])

const updateForm = ref({
    name: props.workspace.name,
    description: props.workspace.description
})

const onSubmit = async (values) => {

}

const isAdmin = computed(() => {
    return props.membershipRole === 'admin'
})

const openLeaveConfirmationModal = ref(false)
const showLeaveConfirmationModal = () => {
    openLeaveConfirmationModal.value = true
}
</script>

<template>
    <WorkspaceSettingsLayout :workspace="props.workspace" :currentUser="props.currentUser" page="general">
        <div class="grid grid-cols-2 px-5 mt-3">
            <div class="font-semibold">General Setting</div>
            <div>
                <Form name="updateForm" :model="updateForm" layout="vertical" @finish="onSubmit" :disabled="!isAdmin">
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
                    <Button danger class="mt-2" :icon="h(LogoutOutlined)" @click="showLeaveConfirmationModal">Leave workspace</Button>
                </CollapsePanel>

                <CollapsePanel key="delete" header="Delete workspace" :collapsible="isAdmin ? 'header' : 'disabled'">
                    <div class="text-gray-500">Please proceed with extreme caution. Deleting this workspace will
                        permanently erase all
                        associated data, boards, and pages. Members will lose access immediately, and the workspace
                        cannot be recovered. If you are certain of this decision, please confirm before proceeding.
                    </div>
                    <Button danger class="mt-2" :icon="h(DeleteOutlined)" type="primary">Delete workspace</Button>
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
</template>