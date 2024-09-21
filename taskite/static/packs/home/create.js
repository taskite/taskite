import { createApp } from 'vue'
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import CreateApp from '@/components/home/create/index.vue'

const app = createApp(CreateApp)

app.mount('#app')
