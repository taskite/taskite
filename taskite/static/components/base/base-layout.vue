<script setup>
import { ConfigProvider } from 'ant-design-vue';

const theme = {
  token: {
    borderRadius: 3,
    colorPrimary: '#8B5CF6',
    fontFamily: 'Inter, sans-serif',
  },
}
</script>

<template>
    <ConfigProvider :theme="theme">
        <slot></slot>
    </ConfigProvider>
</template>