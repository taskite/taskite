import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys'
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import BoardSettingsStatesApp from '@/components/boards/settings/states/index.vue'
const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(
  BoardSettingsStatesApp,
  camelcaseKeys(props, { deep: true })
)

app.mount('#app')
