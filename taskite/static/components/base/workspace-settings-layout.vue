<script setup>
import WorkspaceLayout from '@/components/base/workspace-layout.vue';
import { ApiOutlined, CreditCardOutlined, ExportOutlined, ProfileOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons-vue';
import { Avatar, TabPane, Tabs } from 'ant-design-vue';
import { ref, computed } from 'vue';
import { generateAvatar } from '@/utils/helpers';

const props = defineProps(['workspace', 'currentUser', 'page'])
const activeKey = ref(props.page)

const switchTab = (key) => {
    var redirectUrl = `/${props.workspace.slug}/settings/${key}/`

    if (key === 'general') {
        redirectUrl = `/${props.workspace.slug}/settings/`
    }

    window.location.href = redirectUrl
}

const getWorkspaceLogo = computed(() => {
    if (props.workspace?.logo) {
        return props.workspace.logo
    }

    return generateAvatar(props.workspace.name, 20)
})

</script>

<template>
    <WorkspaceLayout page="settings" :workspace="props.workspace" :currentUser="props.currentUser">
        <div class="container mx-auto p-2">
            <div class="text-xl font-semibold mb-2">{{ props.workspace.name }}'s settings</div>
            <Tabs v-model:activeKey="activeKey" @change="switchTab">
                <TabPane key="general">
                    <template #tab>
                        <ProfileOutlined />
                        <span>General</span>
                    </template>
                </TabPane>

                <TabPane key="members">
                    <template #tab>
                        <UserOutlined />
                        <span>Members</span>
                    </template>
                </TabPane>

                <TabPane key="teams">
                    <template #tab>
                        <TeamOutlined />
                        <span>Teams</span>
                    </template>
                </TabPane>

                <TabPane key="integrations">
                    <template #tab>
                        <ApiOutlined />
                        <span>Integrations</span>
                    </template>
                </TabPane>

                <TabPane key="billing">
                    <template #tab>
                        <CreditCardOutlined />
                        <span>Billing</span>
                    </template>
                </TabPane>

                <TabPane key="exports">
                    <template #tab>
                        <ExportOutlined />
                        <span>Exports</span>
                    </template>
                </TabPane>
            </Tabs>
            <slot></slot>
        </div>
    </WorkspaceLayout>
</template>