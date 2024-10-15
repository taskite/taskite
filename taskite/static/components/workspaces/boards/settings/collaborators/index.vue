<script setup>
import BoardSettingsLayout from '@/components/base/board-settings-layout.vue';
import { ref } from 'vue';
import { Tabs, TabPane } from 'ant-design-vue';
import { TeamOutlined, UserOutlined } from '@ant-design/icons-vue';
import WorkspaceLayout from '@/components/base/workspace-layout.vue';
import TeamList from '@/components/workspaces/boards/settings/collaborators/team-list.vue';
import UserList from '@/components/workspaces/boards/settings/collaborators/user-list.vue';

const props = defineProps(['workspace', 'board', 'hasEditPermission'])

const activeKey = ref('users')
</script>

<template>
    <WorkspaceLayout :workspace="props.workspace" page="boards">
        <BoardSettingsLayout :workspace="props.workspace" :board="props.board" page="collaborators">
            <div class="flex justify-between items-center mb-3">
                <div class="text-xl">Collaborators</div>
            </div>

            <Tabs v-model:activeKey="activeKey" type="card">
                <TabPane key="users">
                    <template #tab>
                        <span>
                            <UserOutlined />
                            Users
                        </span>
                    </template>

                    <UserList :boardId="props.board.id" :workspaceId="props.workspace.id"
                        :hasEditPermission="props.hasEditPermission" />
                </TabPane>

                <TabPane key="teams">
                    <template #tab>
                        <span>
                            <TeamOutlined />
                            Teams
                        </span>
                    </template>

                    <TeamList :boardId="props.board.id" :workspaceId="props.workspace.id"
                        :hasEditPermission="props.hasEditPermission" />
                </TabPane>
            </Tabs>
        </BoardSettingsLayout>
    </WorkspaceLayout>
</template>