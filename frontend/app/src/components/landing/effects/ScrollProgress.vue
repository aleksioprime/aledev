<template>
  <div class="scroll-progress" aria-hidden="true">
    <div class="scroll-progress__bar" :style="{ transform: `scaleX(${progress})` }"></div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const progress = ref(0)
let ticking = false

function update() {
  const max = document.documentElement.scrollHeight - window.innerHeight
  progress.value = max > 0 ? Math.min(1, window.scrollY / max) : 0
  ticking = false
}

function onScroll() {
  if (ticking) return
  ticking = true
  requestAnimationFrame(update)
}

onMounted(() => {
  update()
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onScroll)
})
</script>

<style scoped>
.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 80;
  height: 2px;
  pointer-events: none;
}

.scroll-progress__bar {
  height: 100%;
  background: var(--grad);
  transform-origin: 0 50%;
  box-shadow: 0 0 12px rgb(34 211 238 / 0.7);
}
</style>
