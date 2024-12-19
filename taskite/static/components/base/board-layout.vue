<script setup>
import { TableOutlined, CalendarOutlined, CarryOutOutlined, SettingOutlined, LeftOutlined, AppstoreOutlined } from '@ant-design/icons-vue';
import { TabPane, Tabs } from 'ant-design-vue';
import { ref } from 'vue';
import BaseLayout from '@/components/base/base-layout.vue';

const props = defineProps(['board', 'workspace', 'page'])

const activeKey = ref(props.page)

const switchTab = (key) => {
    if (key === 'kanban') {
        window.location.href = `/b/${props.board.id}/`
    } else {
        window.location.href = `/b/${props.board.id}/${key}/`
    }
}
</script>

<template>
    <BaseLayout>
        <Tabs v-model:active-key="activeKey" class="pl-5" @change="switchTab">
            <TabPane key="kanban">
                <template #tab>
                    <span>
                        <AppstoreOutlined />
                        Kanban
                    </span>
                </template>
            </TabPane>

            <TabPane key="table">
                <template #tab>
                    <TableOutlined />
                    Table
                </template>
            </TabPane>

            <TabPane key="timeline" disabled>
                <template #tab>
                    <CalendarOutlined />
                    Timeline
                </template>
            </TabPane>

            <TabPane key="sprints">
                <template #tab>
                    <CarryOutOutlined />
                    Sprints
                </template>
            </TabPane>

            <TabPane key="settings">
                <template #tab>
                    <SettingOutlined />
                    Settings
                </template>
            </TabPane>

            <template #rightExtra>
                <slot name="actions"></slot>
            </template>
        </Tabs>
        <div class="pl-5">
            <slot></slot>
        </div>
    </BaseLayout>
</template>