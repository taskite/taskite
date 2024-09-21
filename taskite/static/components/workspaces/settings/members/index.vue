<script setup>
import { h, onMounted, ref } from 'vue';
import { Table, Select, Avatar, Flex, Button, Tag, SelectOption } from 'ant-design-vue'

import WorkspaceSettingsLayout from '@/components/base/workspace-settings-layout.vue';
import { workspaceMembershipsAPI } from '@/utils/api/workspaces';
import { generateAvatar } from '@/utils/helpers';
import dayjs from 'dayjs';
import { CloseOutlined, PlusOutlined } from '@ant-design/icons-vue';

const props = defineProps(['workspace', 'membershipRole', 'pageTitle', 'currentUser'])

const memberships = ref([])
const fetchMemberships = async () => {
    try {
        const { data } = await workspaceMembershipsAPI(props.workspace.id)
        memberships.value = data.map(membership => {
            return {
                key: membership.id,
                ...membership
            }
        })
    } catch (error) {
        console.log(error)
    }
}

const columns = [
    {
        title: 'Name',
        key: 'name'
    },
    {
        title: 'Email',
        key: 'email'
    },
    {
        title: 'Role',
        key: 'role'
    },
    {
        title: 'Teams',
        key: 'teams'
    },
    {
        title: 'Joined',
        key: 'joined'
    },
    {
        title: 'Actions',
        key: 'actions'
    }
]

const handleRoleChange = (membershipId, newRole) => {
    console.log(membershipId)
    console.log(newRole)
}

onMounted(() => {
    fetchMemberships()
})
</script>

<template>
    <WorkspaceSettingsLayout :workspace="props.workspace" page="members" :currentUser="props.currentUser">
        <Flex justify="space-between" class="header">
            <div class="text-2xl">Members</div>

            <div class="flex gap-3">
                <Button>View pending members</Button>
                <Button type="primary" :icon="h(PlusOutlined)">Invite member</Button>
            </div>
        </Flex>
        <Table :columns="columns" :dataSource="memberships" size="small">
            <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'name'">
                    <Flex align="center" gap="middle">
                        <Avatar :src="generateAvatar(record.user.firstName)" />
                        <Flex vertical>
                            <div>
                                {{ record.user.firstName }} {{ record.user?.lastName }}
                            </div>
                            <div class="member-username">@{{ record.user.username }}</div>
                        </Flex>
                    </Flex>
                </template>

                <template v-else-if="column.key === 'email'">
                    {{ record.user.email }}
                </template>

                <template v-else-if="column.key === 'role'">
                    <Select v-model:value="record.role" style="width: 140px"
                        @change="(role) => handleRoleChange(record.id, role)"
                        :disabled="props.membershipRole !== 'admin'">
                        <SelectOption value="collaborator">Collaborator</SelectOption>
                        <SelectOption value="admin">Admin</SelectOption>
                    </Select>
                </template>

                <template v-else-if="column.key === 'teams'">
                    <div v-if="record.user.teams.length === 0">-</div>
                    <div v-else>
                        <Tag :bordered="false" v-for="team in record.user.teams" :key="team.id">{{ team.name }}</Tag>
                    </div>
                </template>

                <template v-else-if="column.key === 'joined'">
                    {{ dayjs(record.createdAt).format('D MMM YY') }}
                </template>

                <template v-else-if="column.key === 'actions'">
                    <Flex gap="middle">
                        <Button type="text" :icon="h(CloseOutlined)" :disabled="props.membershipRole !== 'admin'"
                            class="text-gray-500">
                            Remove
                        </Button>
                    </Flex>
                </template>
            </template>
        </Table>
    </WorkspaceSettingsLayout>
</template>

<style scoped>
.header {
    margin-bottom: 15px;
}

.member-username {
    font-size: small;
    color: gray;
}
</style>