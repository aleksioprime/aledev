<template>
  <section :id="sectionId" class="section">
    <div class="about shell">
      <figure v-reveal="'left'" class="about__photo">
        <div ref="photoRef" class="about__photo-inner">
          <!-- ЗАГЛУШКА: замените файл public/images/placeholders/workspace.svg на своё фото -->
          <img src="/images/placeholders/workspace.svg" :alt="t('about.photoAlt')" loading="lazy" />
        </div>
        <figcaption class="about__badge font-mono">
          <span class="about__pulse"></span>
          {{ t('about.badge') }}
        </figcaption>
      </figure>

      <div class="about__content">
        <header class="section-head">
          <span v-reveal class="section-kicker">01 — {{ t('about.kicker') }}</span>
          <h2 v-reveal="{ delay: 80 }" class="section-title">
            {{ t('about.titleStart') }} <span class="text-gradient">{{ t('about.titleAccent') }}</span>
          </h2>
        </header>

        <p v-reveal="{ delay: 140 }" class="about__lead">{{ t('about.p1') }}</p>
        <p v-reveal="{ delay: 200 }" class="about__text">{{ t('about.p2') }}</p>

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
          <span class="focus__icon mdi" :class="item.icon"></span>
          <h3 class="focus__title">{{ t(`about.focus.${item.key}.title`) }}</h3>
          <p class="focus__text">{{ t(`about.focus.${item.key}.text`) }}</p>
          <span class="focus__num font-mono">0{{ i + 1 }}</span>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import CountUp from '@/components/landing/effects/CountUp.vue'
import { skills } from '@/common/constants/skills'
import { useProjectStore } from '@/stores/project'
import { useExperienceStore } from '@/stores/experience'

const sectionId = 'about'
const { t } = useI18n()

const projectStore = useProjectStore()
const experienceStore = useExperienceStore()

const projectsTotal = ref(0)
const years = ref(0)
const photoRef = ref(null)

const focusAreas = [
  { key: 'backend', icon: 'mdi-server-network' },
  { key: 'frontend', icon: 'mdi-vuejs' },
  { key: 'iot', icon: 'mdi-chip' },
  { key: 'teaching', icon: 'mdi-school-outline' },
]

// Все цифры берутся из реальных данных: API проектов, опыта и списка навыков
const stats = computed(() => [
  { key: 'years', value: years.value, suffix: '+' },
  { key: 'projects', value: projectsTotal.value, suffix: '' },
  { key: 'stack', value: skills.flat().length, suffix: '' },
].filter((s) => s.value > 0))

async function loadStats() {
  const [projects, experience] = await Promise.all([
    projectStore.loadProjects({ params: { offset: 0, limit: 1 } }),
    experienceStore.loadExperiences({ params: { offset: 0, limit: 100 } }),
  ])
  if (projects) projectsTotal.value = projects.total
  if (experience?.items?.length) {
    const first = Math.min(...experience.items.map((e) => new Date(e.start_date).getTime()))
    years.value = Math.max(1, Math.floor((Date.now() - first) / (365.25 * 24 * 3600 * 1000)))
  }
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
  loadStats()
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    window.addEventListener('scroll', onScroll, { passive: true })
    onScroll()
  }
})

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId)
  window.removeEventListener('scroll', onScroll)
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
  background: linear-gradient(180deg, transparent 55%, rgb(6 7 11 / 0.75));
}

.about__photo img {
  width: 100%;
  height: 115%;
  object-fit: cover;
  transform: translate3d(0, var(--py, 0), 0) scale(1.05);
  transition: transform 0.2s linear;
}

.about__badge {
  position: absolute;
  left: 1.25rem;
  bottom: 1.25rem;
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.55rem 0.9rem;
  border: 1px solid var(--line-strong);
  border-radius: 999px;
  background: rgb(10 12 18 / 0.8);
  backdrop-filter: blur(10px);
  font-size: 0.78rem;
}

.about__pulse {
  position: relative;
  width: 0.55rem;
  height: 0.55rem;
  border-radius: 50%;
  background: var(--accent-3);
}

.about__pulse::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: var(--accent-3);
  animation: ping 1.8s var(--ease-out) infinite;
}

@keyframes ping {
  to { transform: scale(3); opacity: 0; }
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
  grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
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
  .focus {
    grid-template-columns: 1fr;
  }
}
</style>
