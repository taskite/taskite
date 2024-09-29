<script setup>
import { Avatar, Card, InputSearch, Button, message } from 'ant-design-vue';
import { computed, h, ref } from 'vue';
import { workspaceMemberSearchAPI, workspaceTeamMembershipsCreateAPI } from '@/utils/api';
import { generateAvatar } from '@/utils/helpers';
import { PlusOutlined } from '@ant-design/icons-vue';

const props = defineProps(['workspace', 'team', 'members'])
const emit = defineEmits(['membershipAdded'])

const existingMemberIds = computed(() => {
    return props.members.map(m => m.id)
})

const searchValue = ref('')
const searchMembers = ref([])
const onSearch = async (value) => {
    if (!value) return

    try {
        const { data } = await workspaceMemberSearchAPI(props.workspace.id, value)
        searchMembers.value = data
    } catch (error) {
        console.log(error)
    }
}

const createTeamMembership = async (memberId) => {
    const postData = {
        memberId,
        teamId: props.team.id
    }

    try {
        const { data } = await workspaceTeamMembershipsCreateAPI(props.workspace.id, postData)
        message.success(`${data.user.firstName} ${data.user?.lastName} has been added to the team.`)
        emit('membershipAdded', data)
    } catch (error) {
        console.log(error)
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
                <Button v-if="existingMemberIds.includes(member.id)" disabled type="text">Already present</Button>
                <Button v-else type="text" :icon="h(PlusOutlined)" @click="createTeamMembership(member.id)">Add</Button>
            </div>
        </div>
    </Card>
</template>