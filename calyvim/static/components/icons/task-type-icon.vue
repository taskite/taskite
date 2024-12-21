<script setup>
import { CheckSquareTwoTone, PlaySquareTwoTone, DownSquareTwoTone, PlusSquareTwoTone } from '@ant-design/icons-vue';

const props = defineProps(['taskType'])
</script>

<template>
    <CheckSquareTwoTone two-tone-color="#8B5CF6" v-if="props.taskType === 'issue'" />
    <PlaySquareTwoTone two-tone-color="#8B5CF6" v-else-if="props.taskType === 'story'" />
    <DownSquareTwoTone two-tone-color="#8B5CF6" v-else-if="props.taskType === 'bug'" />
    <PlusSquareTwoTone two-tone-color="#8B5CF6" v-else-if="props.taskType === 'feature'" />
</template>