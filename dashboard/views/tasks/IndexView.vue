<script setup>
import { stateListAPI } from '@/utils/api';
import { useDragAndDrop } from '@formkit/drag-and-drop/vue'
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
const route = useRoute()

const [parent, tapes] = useDragAndDrop([
  'Depeche Mode',
  'Duran Duran',
  'Pet Shop Boys',
  'Kraftwerk',
  'Tears for Fears',
  'Spandau Ballet',
])

const fetchStates = async () => {
    try {
        await stateListAPI(route.params.boardId)
    } catch (error) {
        console.log(error)
    }
}

onMounted(async () => {
    await fetchStates()
})
</script>

<template>
  <ul ref="parent">
    <li v-for="tape in tapes" :key="tape" class="cassette">
      {{ tape }}
    </li>
  </ul>
</template>
