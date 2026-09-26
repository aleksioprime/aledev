<template>
  <div v-if="enabled" class="cursor-layer" aria-hidden="true">
    <div ref="glowRef" class="cursor-glow"></div>
    <div ref="dotRef" class="cursor-dot" :class="{ 'is-hover': hovering }"></div>
  </div>
</template>

<script setup>
// Мягкое свечение и «кольцо», которое с инерцией догоняет курсор.
// Над ссылками и кнопками кольцо увеличивается. Только для мыши.
import { onBeforeUnmount, onMounted, ref } from 'vue'

const glowRef = ref(null)
const dotRef = ref(null)
const enabled = ref(false)
const hovering = ref(false)

const target = { x: -200, y: -200 }
const glow = { x: -200, y: -200 }
const dot = { x: -200, y: -200 }
let rafId = 0

function onMove(e) {
  target.x = e.clientX
  target.y = e.clientY
  hovering.value = !!e.target.closest?.('a, button, [role="button"], input, textarea')
}

function loop() {
  glow.x += (target.x - glow.x) * 0.08
  glow.y += (target.y - glow.y) * 0.08
  dot.x += (target.x - dot.x) * 0.25
  dot.y += (target.y - dot.y) * 0.25
  if (glowRef.value) glowRef.value.style.transform = `translate3d(${glow.x}px, ${glow.y}px, 0)`
  if (dotRef.value) dotRef.value.style.transform = `translate3d(${dot.x}px, ${dot.y}px, 0)`
  rafId = requestAnimationFrame(loop)
}

onMounted(() => {
  const fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (!fine || reduced) return
  enabled.value = true
  window.addEventListener('pointermove', onMove, { passive: true })
  rafId = requestAnimationFrame(loop)
})

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId)
  window.removeEventListener('pointermove', onMove)
})
</script>

<style scoped>
.cursor-layer {
  position: fixed;
  inset: 0;
  z-index: 70;
  pointer-events: none;
}

.cursor-glow {
  position: absolute;
  top: -300px;
  left: -300px;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  background: radial-gradient(circle, rgb(34 211 238 / 0.07), rgb(167 139 250 / 0.04) 40%, transparent 70%);
  mix-blend-mode: screen;
}

.cursor-dot {
  position: absolute;
  top: -14px;
  left: -14px;
  width: 28px;
  height: 28px;
  border: 1px solid rgb(34 211 238 / 0.7);
  border-radius: 50%;
  transition: width 0.3s var(--ease-out), height 0.3s var(--ease-out), top 0.3s var(--ease-out), left 0.3s var(--ease-out), background-color 0.3s ease, border-color 0.3s ease;
}

.cursor-dot.is-hover {
  top: -28px;
  left: -28px;
  width: 56px;
  height: 56px;
  border-color: rgb(167 139 250 / 0.8);
  background: rgb(167 139 250 / 0.08);
}
</style>
