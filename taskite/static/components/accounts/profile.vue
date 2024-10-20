<script setup>
import { onMounted, ref } from 'vue'
import { Form, Input, Button, Avatar, FormItem, Upload, message } from 'ant-design-vue'
import { UserOutlined, MailOutlined, CloseOutlined } from '@ant-design/icons-vue'
import { generateAvatar } from '@/utils/helpers';
import { uploadRequestHandler, handleResponseError } from '@/utils/helpers';
import { accountsProfileAPI, accountsProfileUpdateAPI } from '@/utils/api';
import BaseLayout from '@/components/base/base-layout.vue';

const formState = ref({
    username: '',
    email: '',
    firstName: '',
    lastName: '',
    avatar: null,
    avatarSrc: null
})

const handleAvatarUpload = async (options) => {
    const { fileKey, fileSrc } = await uploadRequestHandler(options, "User", "avatar")
    
    formState.value.avatar = fileKey
    formState.value.avatarSrc = fileSrc
}

const removeAvatar = () => {
    formState.value.avatar = null
    formState.value.avatarSrc = null
}

const onFinish = async (values) => {
    try {
        await accountsProfileUpdateAPI(values)
        message.success('Profile updated successfully!')
    } catch (error) {
        handleResponseError(error)
    }
}

const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo)
}

const goToDashboard = () => {
    window.location.href = `/w`
}

const fetchUserProfile = async () => {
    try {
        const { data } = await accountsProfileAPI()
        formState.value = {
            ...data,
        }
    } catch (error) {
        handleResponseError(error)
    }
}

onMounted(() => {
    fetchUserProfile()
})
</script>

<template>
    <BaseLayout>
        <div class="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
            <div class="relative py-3 sm:max-w-xl sm:mx-auto">
                <div
                    class="absolute inset-0 bg-gradient-to-r from-primary to-light-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-xl">
                </div>
                <div class="relative px-4 py-10 bg-white shadow-lg sm:rounded-xl sm:p-20">
                    <div class="max-w-md mx-auto">
                        <h1 class="text-2xl font-semibold mb-6">Update Your Profile</h1>
                        <Form :model="formState" layout="vertical" name="profileForm" @finish="onFinish"
                            @finishFailed="onFinishFailed" hide-required-mark autocomplete="off">
                            <FormItem name="avatar">
                                <div class="flex flex-col items-start gap-2">
                                    <Upload :multiple="false" name="file" :customRequest="handleAvatarUpload"
                                        :show-upload-list="false">
                                        <Avatar :size="80"
                                            :src="!!formState.avatarSrc ? formState.avatarSrc : generateAvatar(formState.firstName)">
                                            <template #icon>
                                                <PlusOutlined />
                                            </template>
                                        </Avatar>
                                    </Upload>
                                    <div class="flex items-center space-x-2 cursor-pointer text-xs"
                                        @click="removeAvatar" v-if="!!formState.avatarSrc">
                                        <CloseOutlined />
                                        <span>Remove</span>
                                    </div>
                                </div>
                            </FormItem>
                            <FormItem label="Email">
                                <Input v-model:value="formState.email" placeholder="Email" disabled>
                                <template #prefix>
                                    <mail-outlined class="site-form-item-icon" />
                                </template>
                                </Input>
                            </FormItem>
                            <FormItem name="username" label="Username"
                                :rules="[{ required: true, message: 'Please input your username!' }]">
                                <Input v-model:value="formState.username" placeholder="Username">
                                <template #prefix>
                                    <user-outlined class="site-form-item-icon" />
                                </template>
                                </Input>
                            </FormItem>
                            <FormItem name="firstName" label="First name"
                                :rules="[{ required: true, message: 'Please input your first name!' }]">
                                <Input v-model:value="formState.firstName" placeholder="First Name">
                                <template #prefix>
                                    <user-outlined class="site-form-item-icon" />
                                </template>
                                </Input>
                            </FormItem>
                            <FormItem name="lastName" label="Last name">
                                <Input v-model:value="formState.lastName" placeholder="Last Name">
                                <template #prefix>
                                    <user-outlined class="site-form-item-icon" />
                                </template>
                                </Input>
                            </FormItem>
                            <FormItem>
                                <div class="flex justify-between items-center">
                                    <Button type="text" @click="goToDashboard">
                                        ← Back to Dashboard
                                    </Button>
                                    <Button type="primary" html-type="submit">
                                        Update Profile
                                    </Button>
                                </div>
                            </FormItem>
                        </Form>
                    </div>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>

<style>
/* You may need to import Ant Design CSS or use a plugin to do so */
/* @import 'ant-design-vue/dist/antd.css'; */
</style>