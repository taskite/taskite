<script setup>
import { Timeline, TimelineItem } from 'ant-design-vue'
import { MessageOutlined, PushpinOutlined } from '@ant-design/icons-vue'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

const props = defineProps(['boardId', 'taskId', 'comments'])
</script>

<template>
  <Timeline>
    <TimelineItem v-for="comment in props.comments" :key="comment.id">
      <template #dot>
        <template v-if="comment.commentType === 'update'">
          <MessageOutlined />
        </template>
        <template v-else>
          <PushpinOutlined />
        </template>
      </template>

      <template v-if="comment.commentType === 'update'">
        <div class="flex flex-col gap-1">
          <div>
            <span class="font-semibold text-[12px]">
              {{ comment.author.displayName }}
            </span>
            <span class="text-[12px]"> commented. </span>
            <span class="text-[12px]">
              {{ dayjs(comment.createdAt).fromNow() }}
            </span>
          </div>
          <div class="text-[14px]">{{ comment.content }}</div>
        </div>
      </template>
      <template v-else>
        <span class="font-semibold text-[12px] mr-1">
          {{ comment.author.displayName }}
        </span>
        <span class="text-[12px] mr-1"> {{ comment.content }} </span>
        <span class="text-[12px]">
          {{ dayjs(comment.createdAt).fromNow() }}
        </span>
      </template>
    </TimelineItem>
  </Timeline>
</template>
