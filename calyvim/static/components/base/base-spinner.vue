<template>
  <spin :indicator="indicator" />
</template>

<script lang="ts" setup>
import { LoadingOutlined } from '@ant-design/icons-vue'
import { Spin } from 'ant-design-vue'
import { h } from 'vue'

const indicator = h(LoadingOutlined, {
  style: {
    fontSize: '24px',
    // animation: 'antRotate 0.5s infinite linear', // Changed from default 1s to 0.5s
  },
  spin: true,
})
</script>

<style scoped>
/* @keyframes antRotate {
  to {
    transform: rotate(360deg);
  }
} */
</style>
