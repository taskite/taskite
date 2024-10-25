<script setup>
import { h, onMounted, ref } from 'vue'
import { Form, Input, Button, Avatar, FormItem, Upload, message, Textarea } from 'ant-design-vue'
import { SaveOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons-vue'
import { generateAvatar } from '@/utils/helpers';
import { uploadRequestHandler, handleResponseError } from '@/utils/helpers';
import { accountsProfileAPI, accountsProfileUpdateAPI } from '@/utils/api';
import AccountSettingsLayout from '@/components/base/account-settings-layout.vue';

const formState = ref({
    username: '',
    email: '',
    firstName: '',
    lastName: '',
    avatar: null,
    avatarSrc: null,
    bio: '',
    displayName: ''
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
        const { data } = await accountsProfileUpdateAPI(values)
        localStorage.setItem('currentUser', JSON.stringify(data))
        message.success('Profile updated successfully!')
    } catch (error) {
        handleResponseError(error)
    }
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
    <AccountSettingsLayout page="profile">
        <Form :model="formState" name="profileForm" layout="vertical" @finish="onFinish">
            <FormItem name="avatar">
                <div class="relative inline-block group">
                    <Avatar :src="formState.avatar ? formState.avatarSrc : generateAvatar(formState.firstName, 10)"
                        :size="84" shape="square" />
                    <div
                        class="absolute inset-0 bg-black/30 rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center gap-2">
                        <Upload :multiple="false" name="file" :customRequest="handleAvatarUpload"
                            :show-upload-list="false">
                            <Button type="link" :icon="h(EditOutlined)" size="small" />
                        </Upload>
                        <Button type="text" :icon="h(DeleteOutlined)" @click="removeAvatar" danger size="small" />
                    </div>
                </div>
            </FormItem>
            <div class="mb-3">
                <div class="text-xl">{{ formState.firstName }} {{ formState?.lastName }}</div>
                <div class="text-sm font-semibold">{{ formState.email }}</div>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <FormItem label="First name" name="firstName">
                    <Input v-model:value="formState.firstName" />
                </FormItem>

                <FormItem label="Last name" name="lastName">
                    <Input v-model:value="formState.lastName" />
                </FormItem>

            </div>
            <div class="grid grid-cols-2 gap-4">
                <FormItem label="Username" name="username">
                    <Input v-model:value="formState.username" />
                </FormItem>

                <FormItem label="Display name" name="displayName">
                    <Input v-model:value="formState.displayName" />
                </FormItem>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <FormItem label="Bio" name="bio">
                    <Textarea v-model:value="formState.bio" :rows="3" />
                </FormItem>
            </div>

            <div class="flex justify-end">
                <Button type="primary" :icon="h(SaveOutlined)" html-type="submit">Save changes</Button>
            </div>
        </Form>
    </AccountSettingsLayout>
</template>

<style scoped></style>