import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import WorkspaceDashboardApp from '@/components/workspaces/dashboard/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(WorkspaceDashboardApp, camelcaseKeys(props, { deep: true }))

app.mount('#app')