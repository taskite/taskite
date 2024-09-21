import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import WorkspaceSettingsGeneralApp from '@/components/workspaces/settings/general/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(WorkspaceSettingsGeneralApp, camelcaseKeys(props, { deep: true }))

app.mount('#app')
