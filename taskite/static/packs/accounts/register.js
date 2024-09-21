import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import RegisterApp from '@/components/accounts/register.vue'
// const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(RegisterApp)

app.mount('#app')
