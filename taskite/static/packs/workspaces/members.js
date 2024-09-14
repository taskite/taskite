import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import WorkspaceMembersApp from '@/components/workspaces/members/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(WorkspaceMembersApp, camelcaseKeys(props, { deep: true }))

app.mount('#app')
