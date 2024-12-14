<script setup>
import { h, onMounted, ref, watch } from 'vue'
import {
  Skeleton,
  Avatar,
  Button,
  Radio,
  RadioGroup,
  Divider,
  Dropdown,
  Menu,
  MenuItem,
  Upload,
  message,
  Modal,
} from 'ant-design-vue'
import { handleResponseError, generateAvatar } from '@/utils/helpers'
import { useKanbanStore } from '@/stores/kanban'
import TaskCommentList from './task-comment-list.vue'
import SubTaskAddForm from './sub-task-add-form.vue'
import {
  taskCommentsAPI,
  taskCommentsLastAPI,
  taskAttachmentsDeleteAPI,
  taskDetailAPI,
  taskUpdateAPI,
} from '@/utils/api'
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
  PlusOutlined,
  SwitcherOutlined,
  LinkOutlined,
  CheckSquareOutlined,
  FileOutlined,
} from '@ant-design/icons-vue'
import TaskActionBar from './task-action-bar.vue'
import TaskCommentAddForm from './task-comment-add-form.vue'
import {
  taskAttachmentsCreateAPI,
  taskAttachmentsListAPI,
  taskCreateAPI,
} from '../../../../utils/api'
import { uploadRequestHandler } from '../../../../utils/helpers'
import TaskAttachmentList from './task-attachment-list.vue'

dayjs.extend(relativeTime)

const store = useKanbanStore()
const props = defineProps(['board', 'workspace', 'taskId'])

const loading = ref(false)
const updateLoading = ref(false)

const selectedCommentType = ref('update')

const logComment = (commentsData) => {
  if (
    selectedCommentType.value === 'activity' ||
    selectedCommentType.value === 'all'
  ) {
    comments.value.unshift(...commentsData)
  }
}

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

    logComment(data.comments)

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

const attachments = ref([])
const loadAttachments = async () => {
  try {
    const { data } = await taskAttachmentsListAPI(props.board.id, props.taskId)
    attachments.value = data
  } catch (error) {
    handleResponseError(error)
  }
}

const loadTaskDetails = async () => {
  loading.value = true
  await loadTask()
  await loadComments()
  await loadAttachments()
  loading.value = false
}

const updateSummary = (event) => {
  updateTask({ summary: event.target.innerText })
}

// Debounce the updateSummary function with a 1s delay
const debouncedUpdateSummary = debounce(updateSummary, 1000)

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

const addNewComment = (newComment) => {
  if (
    selectedCommentType.value == 'all' ||
    selectedCommentType.value == 'update'
  ) {
    comments.value.unshift(newComment)
  }
}

onMounted(() => {
  loadTaskDetails()
})

const showSubtaskAddForm = ref(false)
const openSubtaskAddForm = () => {
  showSubtaskAddForm.value = true
}
const closeSubtaskAddForm = () => {
  showSubtaskAddForm.value = false
}
const createSubtask = async (subtaskData) => {
  try {
    const { data } = await taskCreateAPI(props.board.id, {
      ...subtaskData,
      parentId: props.taskId,
      assignees: [],
    })
  } catch (error) {
    handleResponseError(error)
  } finally {
    closeSubtaskAddForm()
  }
}

watch(
  () => store.selectedTask,
  () => {
    loadTaskDetails()
  }
)

const createAttachment = async (options) => {
  const { fileKey, fileSrc } = await uploadRequestHandler(
    options,
    'TaskAttachment',
    'attachment'
  )

  try {
    const { data } = await taskAttachmentsCreateAPI(
      props.board.id,
      props.taskId,
      {
        attachment: fileKey,
        filename: options.file.name,
        mimeType: options.file.type,
      }
    )
    attachments.value.push({
      ...data.attachment,
      attachment: fileSrc,
    })
    message.success(`You have added an attachment to ${task.value.name}`)
    logComment([data.comment])
  } catch (error) {
    handleResponseError(error)
  }
}

const deleteAttachment = async (attachmentId) => {
  try {
    const { data } = await taskAttachmentsDeleteAPI(
      props.board.id,
      props.taskId,
      attachmentId
    )
    attachments.value = attachments.value.filter(
      (attachment) => attachment.id !== attachmentId
    )
    message.success('You have removed an attachment')
    logComment([data.comment])
  } catch (error) {
    console.log(error)
    handleResponseError(error)
  }
}
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
        <div class="text-base font-semibold">Description</div>
        <div>
          <TextEditor
            v-model="task.description"
            @update:modelValue="showDescriptionActionButton"
            @saved="updateDescription"
          />
        </div>

        <div class="mb-4">
          <TaskAttachmentList
            :boardId="props.board.id"
            :taskId="props.taskId"
            :attachments="attachments"
            @delete="deleteAttachment"
          />
        </div>

        <div class="mb-4">
          <!-- Subtasks -->
        </div>

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

          <TaskCommentAddForm
            :boardId="props.board.id"
            :taskId="props.taskId"
            @added="addNewComment"
          />

          <TaskCommentList
            :boardId="props.board.id"
            :taskId="props.taskId"
            :comments="comments"
          />
        </div>
      </div>
      <div class="col-span-3">
        <div class="mb-5">
          <Dropdown :trigger="['click']" placement="left">
            <Button :icon="h(PlusOutlined)" class="w-full" type="primary"
              >Add</Button
            >
            <template #overlay>
              <Menu>
                <MenuItem key="subtask" @click="openSubtaskAddForm">
                  <SwitcherOutlined />
                  Subtask
                </MenuItem>

                <MenuItem key="attachment">
                  <Upload
                    :multiple="false"
                    name="file"
                    :customRequest="createAttachment"
                  >
                    <template #itemRender="{ file, actions }">
                      <!-- Don't render anything -->
                    </template>
                    <FileOutlined />
                    Attachment
                  </Upload>
                </MenuItem>

                <MenuItem key="checklist" disabled>
                  <CheckSquareOutlined />
                  Checklist (Coming Soon)
                </MenuItem>

                <MenuItem key="link" disabled>
                  <LinkOutlined />
                  Link (Coming Soon)
                </MenuItem>
              </Menu>
            </template>
          </Dropdown>
        </div>
        <TaskActionBar
          :task="task"
          @updateProperties="(updatedData) => updateTask(updatedData)"
          @updateState="(stateId) => updateState(stateId)"
        />
      </div>
    </div>

    <!-- Subtask Add Form -->
    <Modal
      v-model:open="showSubtaskAddForm"
      title="Add subtask"
      :footer="null"
      centered
      destroyOnClose
      width="700px"
    >
      <SubTaskAddForm :task="task" :boardId="props.board.id" />
    </Modal>
  </div>
  <div v-else>
    <Skeleton />
  </div>
</template>

<style scoped></style>
