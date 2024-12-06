<script setup>
import { h } from 'vue'
import { Avatar, Button } from 'ant-design-vue'
import {
  DownloadOutlined,
  FileOutlined,
  CloseOutlined,
} from '@ant-design/icons-vue'
const props = defineProps(['boardId', 'taskId', 'attachments'])
const emit = defineEmits(['delete'])

function downloadFile(fileUrl, fileName) {
  const link = document.createElement('a')
  link.download = fileName || fileUrl.split('/').pop() // Use the filename or fallback to URL filename
  link.href = fileUrl
  link.click()
}
</script>

<template>
  <div v-if="props.attachments.length > 0">
    <div class="text-base font-semibold mt-3">Attachments</div>
    <div class="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
      <div
        v-for="(attachment, index) in props.attachments"
        :key="index"
        class="relative group rounded-lg overflow-hidden aspect-square"
      >
        <!-- Image or Icon -->
        <template
          v-if="
            attachment.mimeType === 'image/jpeg' ||
            attachment.mimeType === 'image/png'
          "
        >
          <img
            :src="attachment.attachment"
            alt="Thumbnail"
            class="object-cover w-full h-full"
          />
        </template>
        <template v-else>
          <FileOutlined class="text-7xl" />
        </template>

        <!-- Hover Download Button -->
        <div
          class="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity"
        >
          <Button
            size="small"
            type="primary"
            :icon="h(DownloadOutlined)"
            @click="downloadFile(attachment.attachment, attachment.filename)"
          ></Button>
        </div>

        <!-- Delete Badge -->
        <div
          class="absolute top-1 right-1 bg-red-300 text-white rounded-full w-4 h-4 flex items-center justify-center shadow cursor-pointer"
          @click="emit('delete', attachment.id)"
        >
          <CloseOutlined class="text-xs" />
        </div>
      </div>
    </div>
  </div>
</template>
