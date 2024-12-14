<script setup>
import BaseLayout from '@/components/base/base-layout.vue';
import { LeftOutlined, NotificationOutlined, ProfileOutlined, SecurityScanOutlined } from '@ant-design/icons-vue';
import { Layout, Menu, Button } from 'ant-design-vue';
import { ref, h } from 'vue';

const props = defineProps(['page'])

const selectedKeys = ref([props.page])

const changePage = (event) => {
    window.location.href = `/accounts/${event.key}`
}

const redirectBackToDashboard = () => {
    window.location.href = '/'
}
</script>

<template>
    <BaseLayout>
        <Layout>
            <Layout.Sider>
                <div class="p-2">
                    <Button type="text" :icon="h(LeftOutlined)" @click="redirectBackToDashboard">Back to dashboard</Button>
                </div>
                <Menu v-model:selectedKeys="selectedKeys" mode="inline" @select="changePage">
                    <Menu.Item key="profile">
                        <ProfileOutlined />
                        <span>Profile</span>
                    </Menu.Item>
                    
                    <Menu.Item key="security">
                        <SecurityScanOutlined />
                        <span>Security</span>
                    </Menu.Item>

                    <Menu.Item key="notifications" disabled>
                        <NotificationOutlined />
                        <span>Notifications</span>
                    </Menu.Item>
                </Menu>
            </Layout.Sider>

            <Layout>
                <Layout.Content>
                    <div class="container mx-auto px-4 pt-8 max-w-4xl">
                        <slot></slot>
                    </div>
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
    background: #fff;
}

.ant-layout-header {
    background: #fff;
    padding: 0;
    border-bottom: 1px solid gray;
}
</style>