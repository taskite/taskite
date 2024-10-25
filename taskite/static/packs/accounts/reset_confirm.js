import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import ResetConfirmApp from '@/components/accounts/reset-confirm.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(ResetConfirmApp, camelcaseKeys(props, { deep: true }))

app.mount('#app')
