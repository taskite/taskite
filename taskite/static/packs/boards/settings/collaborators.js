import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'


import BoardSettingsMembersApp from '@/components/boards/settings/collaborators/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(BoardSettingsMembersApp, camelcaseKeys(props, { deep: true }))

app.mount('#app')
