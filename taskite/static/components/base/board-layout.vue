<script setup>
import { MenuOutlined, ProjectOutlined, TableOutlined, CalendarOutlined, CarryOutOutlined, SettingOutlined, LeftOutlined, AppstoreOutlined } from '@ant-design/icons-vue';
import { Button, TabPane, Tabs } from 'ant-design-vue';
import { h, ref } from 'vue';
import BaseLayout from '@/components/base/base-layout.vue';

const props = defineProps(['board', 'workspace', 'page'])

const activeKey = ref(props.page)

const switchTab = (key) => {
    if (key === 'kanban') {
        window.location.href = `/${props.workspace.slug}/boards/${props.board.slug}/`
    } else {
        window.location.href = `/${props.workspace.slug}/boards/${props.board.slug}/${key}/`
    }
}

const redirectToBoards = () => {
    window.location.href = `/${props.workspace.slug}/boards/`
}
</script>

<template>
    <BaseLayout>
        <Tabs v-model:active-key="activeKey" class="pl-5" @change="switchTab">
            <template #leftExtra>
                <Button type="text" class="mr-3">{{ props.board.name }}</Button>
            </template>
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

            <TabPane key="sprints" disabled>
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
                <Button type="link" :icon="h(LeftOutlined)" @click="redirectToBoards">Back to boards</Button>
            </template>
        </Tabs>
        <div class="pl-5">
            <slot></slot>
        </div>
    </BaseLayout>
</template>