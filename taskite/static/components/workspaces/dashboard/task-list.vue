<script setup>
import { Table } from 'ant-design-vue';

const props = defineProps(['tasks'])

const columns = [
    {
        name: 'Name',
        key: 'name'
    },
    {
        name: 'Summary',
        key: 'summary'
    }
]
</script>

<template>
    <Table :column="columns" :dataSource="props.tasks" :pagination="false"></Table>
</template>