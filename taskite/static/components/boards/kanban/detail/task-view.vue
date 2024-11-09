<script setup>
import { h, onMounted, ref, watch } from 'vue'
import { Skeleton, Avatar, Button, Radio, RadioGroup, Divider } from 'ant-design-vue'
import { handleResponseError, generateAvatar } from '@/utils/helpers'
import { taskDetailAPI, taskUpdateAPI } from '@/utils/api'
import { useKanbanStore } from '@/stores/kanban'
import TaskCommentList from './task-comment-list.vue'
import SubTasks from './sub-tasks.vue'
import { taskCommentsAPI, taskCommentsLastAPI } from '@/utils/api'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import debounce from 'lodash/debounce'
import TextEditor from '@/components/base/text-editor.vue'
import {
  EllipsisOutlined,
  SaveOutlined,
  ShareAltOutlined,
  SyncOutlined,
  LeftSquareOutlined,
} from '@ant-design/icons-vue'
import TaskActionBar from './task-action-bar.vue'

dayjs.extend(relativeTime)

const store = useKanbanStore()
const props = defineProps(['board', 'workspace', 'taskId'])

const loading = ref(false)
const updateLoading = ref(false)

const selectedCommentType = ref('update')

const updateTask = async (updatedData) => {
  try {
    updateLoading.value = true
    const { data } = await taskUpdateAPI(
      props.board.id,
      props.taskId,
      updatedData
    )
    store.updateTask(data.task)
    task.value = data.task

    if (
      selectedCommentType.value === 'activity' ||
      selectedCommentType.value === 'all'
    ) {
      comments.value.push(...data.comments)
    }

    return data
  } catch (error) {
    handleResponseError(error)
  } finally {
    updateLoading.value = false
  }
}

const task = ref(null)
const loadTask = async () => {
  try {
    const { data } = await taskDetailAPI(props.board.id, props.taskId)
    task.value = {
      ...data,
      oldStateId: data.stateId,
    }
  } catch (error) {
    handleResponseError(error)
  }
}

const updateState = async (stateId) => {
  // Update the task
  try {
    updateLoading.value = true
    const { data } = await taskUpdateAPI(props.board.id, props.taskId, {
      stateId,
    })
    store.updateTaskState(task.value.oldStateId, data.task)
    task.value = {
      ...data.task,
      oldStateId: data.task.stateId,
    }

    const lastCommentRespone = await taskCommentsLastAPI(
      props.board.id,
      props.taskId
    )
    comments.value.push(lastCommentRespone.data)
  } catch (error) {
    handleResponseError(error)
  } finally {
    updateLoading.value = false
  }
}

const comments = ref([])
const loadComments = async () => {
  try {
    const { data } = await taskCommentsAPI(
      props.board.id,
      props.taskId,
      selectedCommentType.value
    )
    comments.value = data.map((comment) => {
      return {
        ...comment,
        key: comment.id,
      }
    })
  } catch (error) {
    handleResponseError(error)
  }
}

const loadTaskDetails = async () => {
  loading.value = true
  await loadTask()
  await loadComments()
  loading.value = false
}

const updateSummary = (event) => {
  updateTask({ summary: event.target.innerText })
}

// Debounce the updateSummary function with a 1s delay
const debouncedUpdateSummary = debounce(updateSummary, 1000)

const descriptionUpdate = (content) => {
  updateTask({ description: content })
}

// Debounce the descriptionUpdate function with a 1s delay
const debouncedDescriptionUpdate = debounce(descriptionUpdate, 2000)

const openDescriptionActionButton = ref(false)
const showDescriptionActionButton = () => {
  openDescriptionActionButton.value = true
}
const closeDescriptionActionButton = () => {
  openDescriptionActionButton.value = false
}

const updateDescription = () => {
  updateTask({ description: task.value.description })
  closeDescriptionActionButton()
}

const handleCommentTypeChange = (e) => {
  loadComments()
}

onMounted(() => {
  loadTaskDetails()
})

watch(
  () => store.selectedTask,
  () => {
    loadTaskDetails()
  }
)
</script>

<template>
  <div v-if="!!task && !loading">
    <div class="mb-4">
      <Button
        :icon="h(LeftSquareOutlined)"
        v-if="!!task.parentId"
        @click="store.setSelectedTask(task.parentId)"
        >Back to parent task</Button
      >
      <div class="flex items-center justify-between">
        <div class="text-xs font-semibold">#{{ task.name }}</div>
        <div class="flex gap-2 items-center">
          <div v-if="updateLoading" class="text-gray-400">
            <SyncOutlined />
            <span class="ml-2">Saving</span>
          </div>
          <Button :icon="h(ShareAltOutlined)" type="text">Share</Button>
          <Button :icon="h(EllipsisOutlined)" type="text"></Button>
        </div>
      </div>
      <div
        class="text-2xl font-semibold mb-1"
        contenteditable="true"
        @input="debouncedUpdateSummary"
      >
        {{ task.summary }}
      </div>
      <div class="text-sm text-gray-500">
        <div class="flex items-center gap-1 text-xs">
          <div>Created</div>
          <div>{{ dayjs(task.createdAt).fromNow() }} by</div>
          <Avatar
            :size="16"
            :src="
              !!task.createdBy.avatar
                ? task.createdBy.avatar
                : generateAvatar(task.createdBy.displayName)
            "
          />
          <div>{{ task.createdBy.displayName }}</div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-12 gap-4">
      <div class="col-span-9">
        <div class="text-lg font-semibold mb-2">Description</div>
        <div>
          <TextEditor
            v-model="task.description"
            @update:modelValue="showDescriptionActionButton"
          />
          <div class="flex gap-2" v-if="openDescriptionActionButton">
            <Button @click="updateDescription" :icon="h(SaveOutlined)"
              >Save</Button
            >
            <Button @click="closeDescriptionActionButton" type="text"
              >Cancel</Button
            >
          </div>
        </div>

        <Divider class="my-3 p-0" />

        <div class="mb-4">
          <SubTasks :boardId="props.board.id" :taskId="task.id" />
        </div>

        <Divider class="my-3 p-0" />

        <div class="mb-6">
          <div class="flex gap-2 items-center justify-between mb-2">
            <div class="text-lg font-semibold mb-2">Activity</div>
            <div>
              <RadioGroup
                v-model:value="selectedCommentType"
                @change="handleCommentTypeChange"
              >
                <Radio value="all">All</Radio>
                <Radio value="update">Updates</Radio>
                <Radio value="activity">Activity</Radio>
              </RadioGroup>
            </div>
          </div>
          <TaskCommentList
            :boardId="props.board.id"
            :taskId="props.taskId"
            :comments="comments"
          />
        </div>
      </div>
      <div class="col-span-3">
        <TaskActionBar
          :task="task"
          @updateProperties="(updatedData) => updateTask(updatedData)"
          @updateState="(stateId) => updateState(stateId)"
        />
      </div>
    </div>
  </div>
  <div v-else>
    <Skeleton />
  </div>
</template>

<style scoped></style>
