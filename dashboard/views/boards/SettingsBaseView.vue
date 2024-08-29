<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <a-layout>
    <a-layout-sider>
      
    </a-layout-sider>
    <a-layout>
      <a-layout-content>
        <RouterView />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>
