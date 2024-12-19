<script setup>
import BoardLayout from '@/components/base/board-layout.vue'
import WorkspaceLayout from '@/components/base/workspace-layout.vue'
import { sprintListAPI } from '../../../../utils/api'
import { handleResponseError } from '../../../../utils/helpers'
import { onMounted, ref } from 'vue'
import BaseSpinner from '../../../base/base-spinner.vue'
import { List, ListItem, ListItemMeta, Tag, Button } from 'ant-design-vue'
import { ArrowRightOutlined, SyncOutlined } from '@ant-design/icons-vue'

const props = defineProps(['workspace', 'board'])

const sprints = ref([])
const loading = ref(false)
const fetchSprint = async () => {
  try {
    loading.value = true
    const { data } = await sprintListAPI(props.board.id)
    sprints.value = data
  } catch (error) {
    handleResponseError(error)
  } finally {
    loading.value = false
  }
}

const openSprintTasks = (sprintId) => {
  window.location.href = `/b/${props.board.id}/sprints/${sprintId}/`
}

onMounted(() => {
  fetchSprint()
})
</script>

<template>
  <WorkspaceLayout :workspace="props.workspace" page="boards">
    <template #default>
      <BoardLayout
        :workspace="props.workspace"
        :board="props.board"
        page="sprints"
      >
        <div v-if="loading" class="flex justify-center items-center h-[80vh]">
          <div class="flex items-center gap-2">
            <BaseSpinner />
            <div>Please wait while we load tasks...</div>
          </div>
        </div>
        <div v-else>
          <List :dataSource="sprints"> <template #renderItem="{ item }">
            <ListItem>
              <div class="flex justify-between w-full">
                <div>
                  <SyncOutlined class="mr-2" />
                  <span>{{ item.name }}</span>
                  <Tag v-if="item.isActive" class="ml-2 text-primary" :bordered="false">Active</Tag>
                </div>

                <div class="flex items-center gap-2">
                  <Tag :bordered="false">
                    <span>{{ item.startDate }}</span>
                    <ArrowRightOutlined />
                    <span>{{ item.endDate }}</span>
                  </Tag>

                  <Button size="small" @click="openSprintTasks(item.id)"><span class="text-xs">View tasks</span></Button>
                </div>
              </div>
            </ListItem>
          </template></List>
        </div>
      </BoardLayout>
    </template>
  </WorkspaceLayout>
</template>
