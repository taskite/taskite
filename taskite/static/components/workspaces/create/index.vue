<script setup>
import BaseLayout from '@/components/base/base-layout.vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import { Button, Form, FormItem, Input, Textarea, Select, SelectOption, Avatar } from 'ant-design-vue';
import { computed, h, ref, watch } from 'vue';
import { workspaceCreareAPI } from '@/utils/api';
import { handleResponseError, generateAvatar, slugify } from '@/utils/helpers';

const createForm = ref({
    name: '',
    description: '',
    slug: '',
    orgSize: null
})

const props = defineProps(['baseUrl'])

const onFinish = async (values) => {
    try {
        const { data } = await workspaceCreareAPI(values)
        window.location.href = `/w/${data.slug}/b`
    } catch (error) {
        handleResponseError(error)
    }
}

const currentUser = computed(() => {
    return JSON.parse(localStorage.getItem("currentUser"))
})

watch(() => createForm.value.name, (newValue) => {
    createForm.value.slug = slugify(newValue)
})
</script>

<template>
    <BaseLayout>
        <div class="min-h-screen bg-gray-100 flex">
            <!-- Left side - can be used for branding or additional content -->
            <div class="w-1/2 hidden lg:block">
                <!-- You can add branding or additional content here -->
            </div>

            <!-- Right side - form and user info -->
            <div class="w-full lg:w-1/2 p-8 relative flex flex-col justify-center">
                <!-- User info and logout in top right corner -->
                <div class="absolute top-4 right-4 flex items-center space-x-4">
                    <div class="flex items-center space-x-2">
                        <div class="text-right">
                            <div class="text-sm font-medium text-gray-900">{{ currentUser?.firstName }} {{ currentUser?.lastName }}</div>
                            <div class="text-xs text-gray-500">{{ currentUser?.email }}</div>
                            <div class="mt-1">
                                <a class="text-xs cursor-pointer underline underline-offset-2" href="/accounts/logout/">Logout</a>
                            </div>
                        </div>
                        <Avatar :src="currentUser?.avatar ? currentUser.avatar : generateAvatar(currentUser?.firstName)" alt="Profile" />
                    </div>
                </div>

                <!-- Form -->
                <div class="max-w-md mx-auto w-full">
                    <h1 class="text-2xl font-bold mb-6">Create your workspace</h1>

                    <Form :model="createForm" layout="vertical" @finish="onFinish">
                        <FormItem label="Workspace Name" name="name" extra="Workspace name can be the name of your organization, company, etc.">
                            <Input v-model:value="createForm.name" />
                        </FormItem>

                        <FormItem label="Workspace URL" name="slug">
                            <Input :addon-before="`${props.baseUrl}/w/`" v-model:value="createForm.slug" />
                        </FormItem>

                        <FormItem label="Organization Size" name="org_size">
                            <Select v-model:value="createForm.orgSize">
                                <SelectOption value="1">Just myself</SelectOption>
                                <SelectOption value="0-10">0 - 10</SelectOption>
                            </Select>
                        </FormItem>

                        <FormItem label="Workspace Description" name="description">
                            <Textarea v-model:value="createForm.description" :rows="4" />
                        </FormItem>

                        <div class="flex justify-end">
                            <FormItem>
                                <div class="flex gap-2">
                                    <Button>Go back</Button>
                                    <Button type="primary" :icon="h(PlusOutlined)" html-type="submit">Create</Button>
                                </div>
                            </FormItem>
                        </div>
                    </Form>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>