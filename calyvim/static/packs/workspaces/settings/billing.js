import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import WorkspaceSettingsBillinglApp from '@/components/workspaces/settings/billing/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(WorkspaceSettingsBillinglApp, camelcaseKeys(props, { deep: true }))

app.mount('#app')
