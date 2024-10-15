<script setup>
import { Avatar, Button, Card, InputSearch } from 'ant-design-vue';
import { computed, h, ref } from 'vue';
import { generateAvatar, handleResponseError } from '@/utils/helpers';
import { PlusOutlined } from '@ant-design/icons-vue';
import { boardPermissionCreateAPI, workspaceMemberSearchAPI } from '@/utils/api';

const props = defineProps(['workspaceId', 'users', 'boardId'])
const emit = defineEmits(['userAdded'])

const existingUserIds = computed(() => props.users.map(user => user.id))

const searchValue = ref('')
const searchMembers = ref([])
const onSearch = async (value) => {
    if (!value) return

    try {
        const { data } = await workspaceMemberSearchAPI(props.workspaceId, value)
        searchMembers.value = data
    } catch (error) {
        handleResponseError(error)
    }
}

const createBoardPermission = async (userId) => {
    try {
        const postData = {
            userId: userId,
            role: 'collaborator'
        }

        const { data } = await boardPermissionCreateAPI(props.boardId, postData)

        emit('userAdded', data)
    } catch (error) {
        handleResponseError(error)
    }
}
</script>

<template>
    <InputSearch v-model:value="searchValue" @search="onSearch" class="mb-2" placeholder="Search members" />
    <div v-if="searchMembers.length > 0" class="text-xs mb-1">Search results ...</div>
    <Card size="small w-full mb-1" v-for="member in searchMembers" :key="member.id">
        <div class="flex justify-between items-center">
            <div class="flex gap-2 items-center">
                <Avatar :src="!!member.avatar ? member.avatar : generateAvatar(member.firstName, 10)" shape="square" />
                <div class="flex flex-col">
                    <div>{{ member.firstName }} {{ member?.lastName }}</div>
                    <div class="text-xs">{{ member.email }}</div>
                </div>
            </div>

            <div>
                <Button v-if="existingUserIds.includes(member.id)" disabled type="text">Already present</Button>
                <Button v-else type="text" :icon="h(PlusOutlined)"
                    @click="createBoardPermission(member.id)">Add</Button>
            </div>
        </div>
    </Card>
</template>