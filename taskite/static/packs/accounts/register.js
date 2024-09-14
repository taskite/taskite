import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'

import RegisterApp from '@/components/accounts/register.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(RegisterApp, camelcaseKeys(props, { deep: true }))

app.mount('#app')
