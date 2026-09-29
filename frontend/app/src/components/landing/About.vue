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
          <span v-reveal class="section-kicker">01 - {{ t('about.kicker') }}</span>
          <h2 v-reveal="{ delay: 80 }" class="section-title">
            {{ t('about.titleStart') }} <span class="text-gradient">{{ t('about.titleAccent') }}</span>
          </h2>
        </header>

        <p v-reveal="{ delay: 140 }" class="about__lead">{{ t('about.p1') }}</p>

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
        </figure>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import Icon from '@/components/ui/Icon.vue'
import { mdiChevronLeft, mdiChevronRight, mdiClose } from '@mdi/js'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
const sectionId = 'about'
const { t } = useI18n()

const photoRef = ref(null)
const activePhoto = ref(0)
const isPreviewOpen = ref(false)
const photoSlides = [
  { src: '/images/placeholders/about-01.svg' },
  { src: '/images/placeholders/about-02.svg' },
  { src: '/images/placeholders/about-03.svg' },
  { src: '/images/placeholders/about-04.svg' },
  { src: '/images/placeholders/about-05.svg' },
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
/* Отступ от бегущей строки над секцией */
.section {
  padding-top: clamp(4rem, 9vw, 7rem);
}

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
  background: linear-gradient(180deg, transparent 55%, rgb(var(--bg-rgb) / 0.75));
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
  background: rgb(var(--panel-rgb) / 0.65);
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
  width: min(92vw, 60rem);
  height: min(92svh, 50rem);
  margin: 0;
  cursor: default;
}

.about-preview__figure img {
  display: block;
  width: 100%;
  height: 100%;
  border: 1px solid var(--line-strong);
  border-radius: 0.75rem;
  object-fit: contain;
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
  background: rgb(var(--panel-rgb) / 0.8);
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

@media (max-width: 860px) {
  .about {
    grid-template-columns: 1fr;
  }

  /* Планшетный режим: фото уже всей колонки, но не на всю ширину */
  .about__photo {
    width: 65%;
    margin-inline: auto;
  }
}

@media (max-width: 540px) {
  /* Фотография почти на всю ширину - на телефоне 65% выглядит слишком узко */
  .about__photo {
    width: 90%;
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

}

@media (prefers-reduced-motion: reduce) {
  .about-preview-enter-active,
  .about-preview-leave-active {
    transition: none;
  }
}
</style>
