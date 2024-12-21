import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import WorkspaceBoardApp from '@/components/workspaces/boards/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(WorkspaceBoardApp, camelcaseKeys(props, { deep: true }))

app.mount('#app')
