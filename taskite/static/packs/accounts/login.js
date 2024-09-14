import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'

import LoginApp from '@/components/accounts/login.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(LoginApp, camelcaseKeys(props, { deep: true }))

app.mount('#app')
