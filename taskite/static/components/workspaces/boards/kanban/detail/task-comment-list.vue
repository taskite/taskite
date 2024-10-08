<script setup>
import { Avatar } from 'ant-design-vue';
import { onMounted, ref } from 'vue';
import { taskCommentsAPI } from '@/utils/api';
import { handleResponseError } from '@/utils/helpers';

const props = defineProps(['boardId', 'taskId'])

const comments = ref([])
const loadComments = async () => {
    try {
        const { data } = await taskCommentsAPI(props.boardId, props.taskId)
        comments.value = data.map((comment) => {
            return {
                ...comment,
                key: comment.id
            }
        })
    } catch (error) {
        handleResponseError(error)
    }
}

onMounted(() => {
    loadComments()
})

</script>

<template>
    <h3 class="text-lg font-semibold mb-2">Comments</h3>
    <div v-for="comment in comments" :key="comment.id" class="mb-4 flex items-start space-x-3">
        <Avatar :src="comment.author.avatar" :size="28" :alt="`${comment.author.firstName}'s avatar`" />
        <div class="flex-grow">
            <div class="flex items-center space-x-2 mb-1">
                <span class="font-xs text-gray-450">{{ comment.author.firstName }}</span>
                <span class="text-sm text-gray-800">{{ comment.time }}</span>
            </div>
            <p class="text-gray-600 mb-2">{{ comment.content }}</p>
        </div>
    </div>
</template>