import { createApp } from 'vue'
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import IndexApp from '@/components/home/index.vue'

const app = createApp(IndexApp)

app.mount('#app')
