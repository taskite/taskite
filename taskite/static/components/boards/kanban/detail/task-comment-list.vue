<script setup>
import { Avatar, Timeline, TimelineItem } from 'ant-design-vue';
import { onMounted, ref } from 'vue';
import { taskCommentsAPI } from '@/utils/api';
import { handleResponseError, generateAvatar } from '@/utils/helpers';
import { MessageOutlined, PushpinOutlined, } from '@ant-design/icons-vue';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(relativeTime);

const props = defineProps(['boardId', 'taskId', 'comments'])
</script>

<template>
    <h3 class="text-lg font-semibold mb-2">Comments/Activity</h3>
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

            <template v-if="comment.activityType === 'comment'">
                <div class="flex flex-col gap-1">
                    <div>
                        <span class="font-semibold text-[12px]">{{ comment.author.displayName }}</span> <span class="text-[12px]">commented.</span> <span class="text-[12px]">{{ dayjs(comment.createdAt).fromNow() }}</span>
                    </div>
                    <div class="text-[14px]">{{ comment.content }}</div>
                </div>
            </template>
            <template v-else>
                <span class="font-semibold text-[12px]">{{ comment.author.displayName }}</span> <span class="text-[12px]">{{ comment.content }}</span> <span class="text-[12px]">{{ dayjs(comment.createdAt).fromNow() }}</span>
            </template>

        </TimelineItem>
    </Timeline>
</template>