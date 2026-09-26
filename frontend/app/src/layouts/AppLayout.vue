<template>
  <component :is="layout">
    <slot />
  </component>
</template>

<script setup>
import { shallowRef, watch } from 'vue'
import { useRoute } from 'vue-router'
import layoutMap from './layoutMap'

import logger from '@/common/helpers/logger'

const route = useRoute()
const layout = shallowRef(null)

watch(
  () => route.meta,
  async meta => {
    try {
      layout.value = layoutMap[meta.layout] || layoutMap.default;
      logger.info('Шаблон:', meta.layout || 'default');
    } catch (e) {
      logger.error('Динамический шаблон не найден. Установлен шаблон по-умолчанию.', e);
      layout.value = layoutMap.default;
    }
  }
)

</script>

<style scoped>
.app_layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.content {
  display: flex;
  flex-grow: 1;
}
</style>