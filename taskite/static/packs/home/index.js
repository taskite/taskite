import { createApp } from 'vue'
import 'ant-design-vue/dist/reset.css'

import App from '@/components/home/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(App, props)

app.mount('#app')
