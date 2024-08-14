<script setup>
import { RouterLink, RouterView } from 'vue-router'

const theme = {
  token: {
    fontSize: 13,
    borderRadius: 3,
    colorPrimary: '#6f5c92',
  },
}
</script>

<template>
  <a-config-provider :theme="theme">
    <RouterView />
  </a-config-provider>
</template>

<style scoped></style>
