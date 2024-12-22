import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import VerifyApp from '@/components/accounts/verify.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(VerifyApp, camelcaseKeys(props, { deep: true }))

app.mount('#app')
