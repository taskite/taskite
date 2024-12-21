import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import WorkspaceTeamsApp from '@/components/workspaces/settings/teams/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(WorkspaceTeamsApp, camelcaseKeys(props, { deep: true }))

app.mount('#app')
