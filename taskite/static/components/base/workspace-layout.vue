<script setup>
import { Button, Layout, Menu, Typography, Flex, Avatar, Select, Dropdown, Card, Divider } from 'ant-design-vue'
import { h, ref } from 'vue';
import { DashboardOutlined, LogoutOutlined, SettingOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons-vue';

import BaseLayout from '@/components/base/base-layout.vue';
import { generateAvatar } from '@/utils/helpers';

const props = defineProps(['workspace', 'page', 'pageTitle', 'currentUser'])

const collapsed = ref(false)
const selectedKeys = ref([props.page])

const changePage = (event) => {
    if (event.key === 'dashboard') {
        window.location.href = `/${props.workspace.slug}/`
    } else {
        window.location.href = `/${props.workspace.slug}/${event.key}/`
    }
}
</script>

<template>
    <BaseLayout>
        <Layout>
            <Layout.Sider v-model:collapsed="collapsed" :trigger="null" collapsible>
                <div style="padding: 5px 10px;">
                    <Flex gap="small" justify="space-between" align="center">
                        <div>{{ props.workspace.name }}</div>
                        <Dropdown :trigger="['click']">
                            <Avatar :src="generateAvatar(props.currentUser.firstName, 20)" shape="square" />

                            <template #overlay>
                                <Card size="small">
                                    <div>{{ props.currentUser.email }}</div>
                                    <div>@{{ props.currentUser.username }}</div>
                                    <Button :icon="h(LogoutOutlined)" style="width: 100%;">Logout</Button>
                                </Card>
                            </template>
                        </Dropdown>
                    </Flex>
                </div>
                <Menu v-model:selectedKeys="selectedKeys" mode="inline" @select="changePage">
                    <Menu.Item key="dashboard">
                        <DashboardOutlined />
                        <span>Dashboard</span>
                    </Menu.Item>

                    <Menu.Item key="members">
                        <UserOutlined />
                        <span>Members</span>
                    </Menu.Item>

                    <Menu.Item key="teams">
                        <TeamOutlined />
                        <span>Teams</span>
                    </Menu.Item>

                    <Menu.Item key="settings">
                        <SettingOutlined />
                        <span>Settings</span>
                    </Menu.Item>
                </Menu>
            </Layout.Sider>

            <Layout>
                <!-- <Layout.Header>
                    <Typography.Title :level="3">{{ props.pageTitle }}</Typography.Title>
                </Layout.Header> -->
                <Layout.Content>
                    <slot></slot>
                </Layout.Content>
            </Layout>
        </Layout>
    </BaseLayout>
</template>

<style scoped>
.workspace-header {
    width: 100%;
    margin-bottom: 10px;
    margin-top: 10px;
}

.ant-layout-sider {
    min-height: 100vh;
    background: #fff;
    border-right: 2px solid #8B5CF6;
}

.ant-layout-content {
    padding: 18px;
    background: #fff;
}

.ant-layout-header {
    background: #fff;
    padding: 0;
    border-bottom: 1px solid gray;
}
</style>