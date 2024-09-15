import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import WorkspaceTeamsEditApp from '@/components/workspaces/teams/edit/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(WorkspaceTeamsEditApp, camelcaseKeys(props, { deep: true }))

app.mount('#app')
