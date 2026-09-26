<template>
  <span ref="el">{{ display }}</span>
</template>

<script setup>
// Число, которое «накручивается» при появлении в области видимости.
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps({
  value: { type: Number, required: true },
  duration: { type: Number, default: 1600 },
})

const el = ref(null)
const display = ref(0)
let started = false
let io = null

function run() {
  started = true
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduced) {
    display.value = props.value
    return
  }
  const start = performance.now()
  const tick = (now) => {
    const t = Math.min(1, (now - start) / props.duration)
    const eased = 1 - Math.pow(1 - t, 4)
    display.value = Math.round(props.value * eased)
    if (t < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

watch(() => props.value, () => {
  if (started) run()
})

onMounted(() => {
  io = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting && !started) run()
  }, { threshold: 0.5 })
  io.observe(el.value)
})

onBeforeUnmount(() => io?.disconnect())
</script>
