import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'
import { createPinia } from 'pinia'


import BoardKanbanApp from '@/components/workspaces/boards/kanban/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(BoardKanbanApp, camelcaseKeys(props, { deep: true }))

app.use(createPinia())
app.mount('#app')
