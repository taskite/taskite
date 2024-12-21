import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import VerifyApp from '@/components/accounts/verify.vue'
const app = createApp(VerifyApp)

app.mount('#app')
