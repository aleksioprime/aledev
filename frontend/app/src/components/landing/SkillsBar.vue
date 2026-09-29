<template>
  <section class="marquee-wrap" :aria-label="t('about.stackLabel')">
    <ul class="sr-only">
      <li v-for="skill in skills.flat()" :key="skill">{{ skill }}</li>
    </ul>

    <div v-for="(row, ri) in skills" :key="ri" class="marquee" :class="{ 'marquee--reverse': ri % 2 }"
      aria-hidden="true">
      <div class="marquee__track">
        <template v-for="copy in 3" :key="copy">
          <span v-for="skill in row" :key="`${copy}-${skill}`" class="marquee__item">
            <span class="marquee__star">✦</span>{{ skill }}
          </span>
        </template>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { skills } from '@/common/constants/skills'

const { t } = useI18n()
</script>

<style scoped>
.marquee-wrap {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding-block: 1.5rem;
  border-block: 1px solid var(--line);
  background: rgb(255 255 255 / 0.015);
  transform: rotate(-1.5deg) scale(1.02);
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent);
  mask-image: linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent);
}

.marquee {
  display: flex;
  overflow: hidden;
}

.marquee__track {
  display: flex;
  flex-shrink: 0;
  gap: 1.5rem;
  padding-right: 1.5rem;
  animation: marquee 70s linear infinite;
}

.marquee--reverse .marquee__track {
  animation-direction: reverse;
  animation-duration: 80s;
}

.marquee-wrap:hover .marquee__track {
  animation-play-state: paused;
}

.marquee__item {
  display: inline-flex;
  align-items: center;
  gap: 1.5rem;
  font-family: var(--font-display);
  font-size: clamp(0.95rem, 2.4vw, 1.7rem);
  font-weight: 600;
  letter-spacing: -0.02em;
  white-space: nowrap;
  color: transparent;
  -webkit-text-stroke: 1px rgb(255 255 255 / 0.28);
  transition: color 0.3s ease, -webkit-text-stroke-color 0.3s ease;
}

.marquee--reverse .marquee__item {
  color: rgb(255 255 255 / 0.85);
  -webkit-text-stroke: 0;
}

.marquee__item:hover {
  color: var(--accent);
  -webkit-text-stroke-color: var(--accent);
}

.marquee__star {
  font-size: 0.55em;
  color: var(--accent-2);
  -webkit-text-stroke: 0;
}

@keyframes marquee {
  from { transform: translateX(0); }
  to { transform: translateX(-33.3333%); }
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
}
</style>
