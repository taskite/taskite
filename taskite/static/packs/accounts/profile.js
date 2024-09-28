import { createApp } from 'vue'
import camelcaseKeys from 'camelcase-keys';
import 'ant-design-vue/dist/reset.css'
import '@/assets/base.css'

import ProfileApp from '@/components/accounts/profile.vue'
// const props = JSON.parse(document.getElementById('props').textContent)

const app = createApp(ProfileApp)

app.mount('#app')
