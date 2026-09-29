<template>
  <section :id="sectionId" class="section">
    <div class="about shell">
      <figure v-reveal="'left'" class="about__photo">
        <div ref="photoRef" class="about__photo-inner">
          <button type="button" class="about__photo-open" :aria-label="t('about.openPhoto', { number: activePhoto + 1 })"
            @click="openPhotoPreview">
            <img :key="activePhoto" :src="activeSlide.src" :alt="t('about.photoAlt', { number: activePhoto + 1 })"
              loading="lazy" />
          </button>
        </div>
        <figcaption class="about__badge font-mono">
          <span class="about__pulse"></span>
          {{ activeSlide.stack.join(' · ') }}
        </figcaption>
        <nav class="about__gallery-controls" :aria-label="t('about.galleryLabel')">
          <button type="button" class="gallery-button" :aria-label="t('about.previousPhoto')"
            @click="showPreviousPhoto">
            <Icon :path="mdiChevronLeft" />
          </button>
          <div class="gallery-dots">
            <button v-for="(slide, index) in photoSlides" :key="index" type="button" class="gallery-dot"
              :class="{ 'gallery-dot--active': index === activePhoto }"
              :aria-label="t('about.selectPhoto', { number: index + 1 })" :aria-current="index === activePhoto"
              @click="activePhoto = index" />
          </div>
          <span class="gallery-count font-mono" aria-live="polite">{{ String(activePhoto + 1).padStart(2, '0') }} / 05</span>
          <button type="button" class="gallery-button" :aria-label="t('about.nextPhoto')" @click="showNextPhoto">
            <Icon :path="mdiChevronRight" />
          </button>
        </nav>
      </figure>

      <div class="about__content">
        <header class="section-head">
          <span v-reveal class="section-kicker">01 — {{ t('about.kicker') }}</span>
          <h2 v-reveal="{ delay: 80 }" class="section-title">
            {{ t('about.titleStart') }} <span class="text-gradient">{{ t('about.titleAccent') }}</span>
          </h2>
        </header>

        <p v-reveal="{ delay: 140 }" class="about__lead">{{ t('about.p1') }}</p>

        <dl class="stats">
          <div v-for="(stat, i) in stats" :key="stat.key" v-reveal="{ variant: 'scale', delay: 120 + i * 90 }"
            class="stat">
            <dt class="stat__label">{{ t(`about.stats.${stat.key}`) }}</dt>
            <dd class="stat__value font-display">
              <CountUp :value="stat.value" /><span class="stat__suffix">{{ stat.suffix }}</span>
            </dd>
          </div>
        </dl>
      </div>
    </div>

    <div class="focus shell">
      <div v-for="(item, i) in focusAreas" :key="item.key" v-reveal="{ delay: i * 90 }">
        <article v-tilt="6" class="focus__card glass">
          <span class="focus__icon"><Icon :path="item.icon" /></span>
          <h3 class="focus__title">{{ t(`about.focus.${item.key}.title`) }}</h3>
          <p class="focus__text">{{ t(`about.focus.${item.key}.text`) }}</p>
          <span class="focus__num font-mono">0{{ i + 1 }}</span>
        </article>
      </div>
    </div>
  </section>

  <Teleport to="body">
    <Transition name="about-preview">
      <div v-if="isPreviewOpen" class="about-preview" @click.self="closePhotoPreview">
        <button type="button" class="about-preview__close" :aria-label="t('about.closePhoto')"
          @click="closePhotoPreview">
          <Icon :path="mdiClose" />
        </button>
        <figure class="about-preview__figure">
          <img :src="activeSlide.src" :alt="t('about.photoAlt', { number: activePhoto + 1 })" />
          <figcaption class="font-mono">{{ activeSlide.stack.join(' · ') }}</figcaption>
        </figure>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import Icon from '@/components/ui/Icon.vue'
import { mdiAccountGroupOutline, mdiChevronLeft, mdiChevronRight, mdiChip, mdiClose, mdiServerNetwork, mdiWeb } from '@mdi/js'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import CountUp from '@/components/landing/effects/CountUp.vue'

const sectionId = 'about'
const { t } = useI18n()

const photoRef = ref(null)
const activePhoto = ref(0)
const isPreviewOpen = ref(false)
const EDUCATION_START_YEAR = 2007
const DEVELOPMENT_START_YEAR = 2021
const currentYear = new Date().getFullYear()
const photoSlides = [
  { src: '/images/placeholders/about-01.svg', stack: ['Vue.js', 'FastAPI', 'PostgreSQL'] },
  { src: '/images/placeholders/about-02.svg', stack: ['Docker', 'CI/CD', 'Linux'] },
  { src: '/images/placeholders/about-03.svg', stack: ['Python', 'Computer Vision', 'ML'] },
  { src: '/images/placeholders/about-04.svg', stack: ['Arduino', 'ESP32', 'IoT'] },
  { src: '/images/placeholders/about-05.svg', stack: ['Mentoring', 'Robotics', 'Education'] },
]

const activeSlide = computed(() => photoSlides[activePhoto.value])

function showPreviousPhoto() {
  activePhoto.value = (activePhoto.value + photoSlides.length - 1) % photoSlides.length
}

function showNextPhoto() {
  activePhoto.value = (activePhoto.value + 1) % photoSlides.length
}

function openPhotoPreview() {
  isPreviewOpen.value = true
  window.addEventListener('keydown', handlePreviewKeydown)
}

function closePhotoPreview() {
  isPreviewOpen.value = false
  window.removeEventListener('keydown', handlePreviewKeydown)
}

function handlePreviewKeydown(event) {
  if (event.key === 'Escape') closePhotoPreview()
}

const focusAreas = [
  { key: 'web', icon: mdiWeb },
  { key: 'machineLearning', icon: mdiChip },
  { key: 'iot', icon: mdiServerNetwork },
  { key: 'mentoring', icon: mdiAccountGroupOutline },
]

const stats = [
  { key: 'education', value: currentYear - EDUCATION_START_YEAR, suffix: '+' },
  { key: 'years', value: currentYear - DEVELOPMENT_START_YEAR, suffix: '+' },
]

// Параллакс фото при скролле
let rafId = 0
function onScroll() {
  cancelAnimationFrame(rafId)
  rafId = requestAnimationFrame(() => {
    const el = photoRef.value
    if (!el) return
    const rect = el.getBoundingClientRect()
    const progress = (rect.top + rect.height / 2 - window.innerHeight / 2) / window.innerHeight
    el.style.setProperty('--py', `${progress * -40}px`)
  })
}

onMounted(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const coarse = window.matchMedia('(pointer: coarse)').matches
  if (!reduced && !coarse) {
    window.addEventListener('scroll', onScroll, { passive: true })
    onScroll()
  }
})

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId)
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('keydown', handlePreviewKeydown)
})
</script>

<style scoped>
.about {
  display: grid;
  grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
  align-items: center;
  gap: clamp(2rem, 6vw, 5.5rem);
}

.about__photo {
  position: relative;
  margin: 0;
}

.about__photo-inner {
  position: relative;
  aspect-ratio: 4 / 5;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 2rem;
}

.about__photo-inner::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(180deg, transparent 55%, rgb(6 7 11 / 0.75));
}

.about__photo img {
  position: absolute;
  top: -7.5%;
  left: 0;
  display: block;
  width: 100%;
  height: 115%;
  object-fit: cover;
  transform: translate3d(0, var(--py, 0), 0) scale(1.05);
  transition: transform 0.2s linear;
}

.about__photo-open {
  position: absolute;
  inset: 0;
  z-index: 1;
  width: 100%;
  height: 100%;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: zoom-in;
}

.about__photo-open:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: -4px;
}

.about__badge {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  max-width: 100%;
  margin-top: 0.8rem;
  padding: 0.55rem 0.9rem;
  border: 1px solid var(--line-strong);
  border-radius: 999px;
  background: rgb(10 12 18 / 0.8);
  backdrop-filter: blur(10px);
  font-size: 0.78rem;
}

.about__gallery-controls {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin-top: 0.75rem;
}

.gallery-button {
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  width: 2.5rem;
  aspect-ratio: 1;
  border: 1px solid var(--line-strong);
  border-radius: 50%;
  background: rgb(10 12 18 / 0.65);
  color: var(--text);
  cursor: pointer;
  transition: border-color 0.2s ease, color 0.2s ease;
}

.gallery-button:hover,
.gallery-button:focus-visible {
  border-color: var(--accent);
  color: var(--accent);
}

.gallery-button:focus-visible,
.gallery-dot:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
}

.gallery-dots {
  display: flex;
  flex: 1 1 auto;
  align-items: center;
  justify-content: center;
  gap: 0.55rem;
}

.gallery-dot {
  width: 0.55rem;
  height: 0.55rem;
  flex: 0 0 auto;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: var(--muted);
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.gallery-dot--active {
  background: var(--accent);
  transform: scale(1.2);
}

.gallery-count {
  flex: 0 0 auto;
  font-size: 0.75rem;
  color: var(--muted);
}

.about-preview {
  position: fixed;
  inset: 0;
  z-index: 120;
  display: grid;
  place-items: center;
  padding: clamp(1rem, 4vw, 3rem);
  background: rgb(0 0 0 / 0.84);
  backdrop-filter: blur(10px);
  cursor: zoom-out;
}

.about-preview__figure {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.85rem;
  max-width: 92vw;
  max-height: 92svh;
  margin: 0;
  cursor: default;
}

.about-preview__figure img {
  display: block;
  max-width: 92vw;
  max-height: calc(92svh - 3rem);
  border: 1px solid var(--line-strong);
  border-radius: 0.75rem;
  object-fit: contain;
}

.about-preview__figure figcaption {
  max-width: 100%;
  color: var(--text);
  text-align: center;
}

.about-preview__close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 1;
  display: grid;
  place-items: center;
  width: 2.75rem;
  aspect-ratio: 1;
  border: 1px solid var(--line-strong);
  border-radius: 50%;
  background: rgb(10 12 18 / 0.8);
  color: var(--text);
  cursor: pointer;
}

.about-preview__close:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
}

.about-preview-enter-active,
.about-preview-leave-active {
  transition: opacity 0.2s ease;
}

.about-preview-enter-from,
.about-preview-leave-to {
  opacity: 0;
}

.about__pulse {
  position: relative;
  width: 0.55rem;
  height: 0.55rem;
  border-radius: 50%;
  background: var(--accent-3);
}


.about__lead {
  font-size: clamp(1.15rem, 2vw, 1.35rem);
  line-height: 1.6;
  color: var(--text);
}

.about__text {
  margin-top: 1rem;
  line-height: 1.8;
  color: var(--muted);
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(6.5rem, 1fr));
  gap: 1rem;
  margin-top: 2.5rem;
}

.stat {
  display: flex;
  flex-direction: column-reverse;
  gap: 0.35rem;
  padding: 1.25rem 1.25rem 1.1rem;
  border-left: 1px solid var(--line-strong);
}

.stat__value {
  margin: 0;
  font-size: clamp(2.2rem, 4.5vw, 3.2rem);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.03em;
}

.stat__suffix {
  color: var(--accent);
}

.stat__label {
  font-size: 0.85rem;
  color: var(--muted);
}

/* --- Карточки направлений --- */
.focus {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
  margin-top: clamp(3.5rem, 8vw, 6rem);
}

.focus__card {
  position: relative;
  height: 100%;
  overflow: hidden;
  padding: 1.6rem 1.4rem 1.8rem;
  transition: transform 0.5s var(--ease-out), border-color 0.4s ease;
  transform-style: preserve-3d;
}

.focus__card::before {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(400px circle at var(--mx, 50%) var(--my, 0%), rgb(34 211 238 / 0.12), transparent 45%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.focus__card:hover {
  border-color: rgb(34 211 238 / 0.35);
}

.focus__card:hover::before {
  opacity: 1;
}

.focus__icon {
  display: grid;
  place-items: center;
  width: 3rem;
  height: 3rem;
  margin-bottom: 1.4rem;
  border-radius: 0.9rem;
  background: linear-gradient(135deg, rgb(34 211 238 / 0.18), rgb(167 139 250 / 0.18));
  font-size: 1.5rem;
  color: var(--accent);
}

.focus__title {
  margin-bottom: 0.6rem;
  font-size: 1.1rem;
  font-weight: 700;
}

.focus__text {
  position: relative;
  font-size: 0.92rem;
  line-height: 1.65;
  color: var(--muted);
}

.focus__num {
  position: absolute;
  top: 1.2rem;
  right: 1.3rem;
  font-size: 0.75rem;
  color: rgb(255 255 255 / 0.25);
}

@media (max-width: 1024px) {
  .focus {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 860px) {
  .about {
    grid-template-columns: 1fr;
  }

  .about__photo {
    max-width: 420px;
  }
}

@media (max-width: 540px) {
  .about__badge {
    padding-inline: 0.75rem;
    font-size: 0.7rem;
  }

  .about__gallery-controls {
    gap: 0.4rem;
  }

  .gallery-button {
    width: 2.25rem;
  }

  .gallery-dots {
    gap: 0.45rem;
  }

  .stat {
    padding: 0.9rem 0.75rem 0.8rem;
  }

  .stat__label {
    font-size: 0.75rem;
  }

  .focus {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .about-preview-enter-active,
  .about-preview-leave-active {
    transition: none;
  }
}
</style>
