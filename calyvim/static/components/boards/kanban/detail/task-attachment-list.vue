<script setup>
import { h, computed } from 'vue'
import { Button } from 'ant-design-vue'
import {
  DownloadOutlined,
  FileOutlined,
  MinusOutlined,
  FileWordOutlined,
  FilePdfOutlined,
  FileExcelOutlined,
  FileImageOutlined,
  FileZipOutlined,
  FilePptOutlined,
  FileMarkdownOutlined,
  FileTextOutlined,
  PlayCircleOutlined,
} from '@ant-design/icons-vue'

const props = defineProps(['boardId', 'taskId', 'attachments'])
const emit = defineEmits(['delete'])

const getFileIcon = (mimeType) => {
  const mimeMap = {
    // Microsoft Office
    'application/msword': FileWordOutlined,
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
      FileWordOutlined,
    'application/vnd.ms-excel': FileExcelOutlined,
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
      FileExcelOutlined,
    'application/vnd.ms-powerpoint': FilePptOutlined,
    'application/vnd.openxmlformats-officedocument.presentationml.presentation':
      FilePptOutlined,

    // PDFs
    'application/pdf': FilePdfOutlined,

    // Image (for non-previewable images)
    'image/*': FileImageOutlined,

    // Archives
    'application/zip': FileZipOutlined,
    'application/x-rar-compressed': FileZipOutlined,
    'application/x-7z-compressed': FileZipOutlined,

    // Text & Code
    'text/plain': FileTextOutlined,
    'text/markdown': FileMarkdownOutlined,

    // Audio/Video
    'audio/*': PlayCircleOutlined,
    'video/*': PlayCircleOutlined,

    // Default
    default: FileOutlined,
  }

  // Handle wildcards
  if (mimeType?.startsWith('audio/') || mimeType?.startsWith('video/'))
    return mimeMap['audio/*']
  if (mimeType?.startsWith('image/')) return mimeMap['image/*']

  return mimeMap[mimeType] || mimeMap.default
}

function downloadFile(fileUrl, fileName) {
  const link = document.createElement('a')
  link.download = fileName || fileUrl.split('/').pop()
  link.href = fileUrl
  link.click()
}

const isImage = (mimeType) => {
  return mimeType?.startsWith('image/')
}
</script>

<template>
  <div v-if="props.attachments.length > 0">
    <div class="text-lg font-semibold mt-2">Attachments</div>
    <div class="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-2">
      <div
        v-for="(attachment, index) in props.attachments"
        :key="index"
        class="relative group"
      >
        <div
          class="w-16 h-16 rounded-lg overflow-hidden bg-gray-50 border border-gray-200 flex items-center justify-center transition-all duration-200 group-hover:shadow-sm relative"
        >
          <!-- Image Preview -->
          <img
            v-if="isImage(attachment.mimeType)"
            :src="attachment.attachment"
            :alt="attachment.filename"
            class="w-full h-full object-cover group-hover:opacity-60 transition-opacity"
          />
          <!-- File Icon -->
          <component
            v-else
            :is="getFileIcon(attachment.mimeType)"
            class="text-3xl text-gray-400 group-hover:opacity-60 transition-opacity"
          />

          <!-- Download Button -->
          <div
            class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <DownloadOutlined
              class="text-lg cursor-pointer text-primary hover:text-primary/80"
              @click.stop="
                downloadFile(attachment.attachment, attachment.filename)
              "
            />
          </div>

          <!-- Delete Button -->
          <div
            class="absolute top-1 right-1 w-3 h-3 rounded-full bg-gray-400 opacity-0 group-hover:opacity-70 transition-opacity flex items-center justify-center cursor-pointer hover:opacity-100 hover:bg-red-400"
            @click.stop="emit('delete', attachment.id)"
          >
            <MinusOutlined class="text-[8px] text-white" />
          </div>
        </div>

        <!-- Filename -->
        <div
          class="mt-1 text-xs text-gray-600 truncate max-w-full"
          :title="attachment.filename"
        >
          {{ attachment.filename }}
        </div>
      </div>
    </div>
  </div>
</template>
