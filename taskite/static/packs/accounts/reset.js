import { createApp } from 'vue'
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import ResetApp from '@/components/accounts/reset.vue'
// const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(ResetApp)

app.mount('#app')
