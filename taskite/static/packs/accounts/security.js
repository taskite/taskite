import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import SecurityApp from '@/components/accounts/security.vue'
// const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(SecurityApp)

app.mount('#app')
