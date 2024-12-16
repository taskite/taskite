<script setup>
import { DoubleRightOutlined, FolderOpenOutlined } from '@ant-design/icons-vue';
import { Menu, MenuItem } from 'ant-design-vue'
const props = defineProps(['state'])
</script>

<template>
  <Menu>
    <MenuItem>
        <DoubleRightOutlined />
        <span class="ml-2">Move all tasks to another state</span>
    </MenuItem>
    <MenuItem>
        <FolderOpenOutlined />
        <span class="ml-2">Archive all tasks in the {{ props.state.name }}</span>
    </MenuItem>
  </Menu>
</template>
