<template>
  <!-- Генеративная обложка-заглушка: уникальна для каждого проекта (по его id).
       Когда у проекта появится поле с изображением — передайте его в prop `image`. -->
  <div class="cover" :style="{ '--h1': palette.h1, '--h2': palette.h2 }">
    <img v-if="image" :src="image" :alt="title" loading="lazy" class="cover__img" />
    <svg v-else class="cover__svg" viewBox="0 0 400 225" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <linearGradient :id="`g-${uid}`" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" :stop-color="`hsl(${palette.h1} 80% 55%)`" stop-opacity="0.55" />
          <stop offset="1" :stop-color="`hsl(${palette.h2} 80% 55%)`" stop-opacity="0.15" />
        </linearGradient>
        <pattern :id="`p-${uid}`" width="20" height="20" patternUnits="userSpaceOnUse">
          <circle cx="1" cy="1" r="1" fill="#fff" fill-opacity="0.12" />
        </pattern>
      </defs>
      <rect width="400" height="225" fill="#0b0d14" />
      <rect width="400" height="225" :fill="`url(#g-${uid})`" />
      <rect width="400" height="225" :fill="`url(#p-${uid})`" />
      <g class="cover__traces" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="1.2">
        <path v-for="(d, i) in traces" :key="i" :d="d" />
      </g>
      <g>
        <circle v-for="(n, i) in pads" :key="i" :cx="n.x" :cy="n.y" r="3.2" fill="#0b0d14"
          :stroke="`hsl(${palette.h1} 90% 70%)`" stroke-width="1.5" class="cover__pad"
          :style="{ animationDelay: `${i * 0.35}s` }" />
      </g>
    </svg>
    <span class="cover__mono font-display" aria-hidden="true">{{ monogram }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  seed: { type: String, default: '' },
  title: { type: String, default: '' },
  image: { type: String, default: '' },
})

function hash(str) {
  let h = 2166136261
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i)
    h = Math.imul(h, 16777619)
  }
  return h >>> 0
}

function rng(seed) {
  let s = seed || 1
  return () => {
    s ^= s << 13
    s ^= s >>> 17
    s ^= s << 5
    return ((s >>> 0) % 10000) / 10000
  }
}

const uid = computed(() => hash(props.seed || props.title).toString(36))

const palette = computed(() => {
  const h = hash(props.seed || props.title)
  const h1 = 170 + (h % 110) // от бирюзового до фиолетового
  return { h1, h2: (h1 + 60 + ((h >> 8) % 60)) % 360 }
})

// «Дорожки печатной платы»: ломаные линии под 45°/90°
const geometry = computed(() => {
  const r = rng(hash(props.seed || props.title))
  const traces = []
  const pads = []
  for (let i = 0; i < 7; i++) {
    let x = Math.round(r() * 20) * 20
    let y = Math.round(r() * 11) * 20
    let d = `M${x} ${y}`
    for (let s = 0; s < 3; s++) {
      const len = 40 + Math.round(r() * 4) * 20
      const dir = Math.floor(r() * 4)
      if (dir === 0) x += len
      else if (dir === 1) y += len / 2
      else if (dir === 2) { x += len / 2; y += len / 2 }
      else { x += len / 2; y -= len / 2 }
      d += ` L${x} ${y}`
    }
    traces.push(d)
    pads.push({ x, y })
  }
  return { traces, pads }
})

const traces = computed(() => geometry.value.traces)
const pads = computed(() => geometry.value.pads)

const monogram = computed(() => {
  const words = (props.title || '').replace(/[^\p{L}\p{N}\s]/gu, '').split(/\s+/).filter(Boolean)
  return words.slice(0, 2).map((w) => w[0]).join('').toUpperCase() || '·'
})
</script>

<style scoped>
.cover {
  position: relative;
  overflow: hidden;
  aspect-ratio: 16 / 9;
  background: #0b0d14;
}

.cover__svg,
.cover__img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 1.2s var(--ease-out);
}

.cover__traces path {
  stroke-dasharray: 400;
  stroke-dashoffset: 400;
  animation: trace 3.5s var(--ease-out) forwards;
}

@keyframes trace {
  to { stroke-dashoffset: 0; }
}

.cover__mono {
  position: absolute;
  right: 1rem;
  bottom: 0.2rem;
  font-size: clamp(3rem, 8vw, 5.5rem);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.05em;
  color: transparent;
  -webkit-text-stroke: 1px rgb(255 255 255 / 0.4);
  transition: transform 1s var(--ease-out);
}
</style>
