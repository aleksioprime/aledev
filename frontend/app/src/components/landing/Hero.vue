<template>
  <section :id="sectionId" class="hero">
    <SignalNetwork />

    <div class="hero__inner shell">
      <div class="hero__text">
        <p class="terminal font-mono">
          <span class="terminal__prompt">$</span>
          <span class="terminal__cmd">{{ typedCmd }}</span><span class="terminal__caret"></span>
        </p>

        <h1 class="hero__name font-display" :aria-label="t('hero.name')">
          <span v-for="(word, wi) in nameWords" :key="`${locale}-${wi}`" class="hero__word"
            :class="{ 'text-gradient': wi === nameWords.length - 1 }">
            <span v-for="(ch, ci) in word" :key="ci" class="hero__char" aria-hidden="true"
              :style="{ '--d': `${(wi * 8 + ci) * 38 + 250}ms`, '--i': ci, '--n': word.length }">{{ ch }}</span>
          </span>
        </h1>

        <p class="hero__role font-mono">
          <span class="hero__role-bracket">&lt;</span>
          <span class="hero__role-text">{{ typedRole }}</span><span class="hero__role-caret">|</span>
          <span class="hero__role-bracket">/&gt;</span>
        </p>

        <p class="hero__about">{{ t('hero.about') }}</p>

        <div class="hero__cta">
          <a v-magnetic href="#contacts" class="btn btn-primary" @click.prevent="scrollToSection('contacts')">
            {{ t('hero.contact') }}
            <span class="mdi mdi-arrow-right"></span>
          </a>
          <a v-magnetic :href="cv" target="_blank" rel="noopener" class="btn btn-ghost">
            <span class="mdi mdi-file-download-outline"></span>
            {{ t('hero.download_cv') }}
          </a>
        </div>

        <ul class="hero__socials">
          <li v-for="link in socials" :key="link.label">
            <a :href="link.href" target="_blank" rel="noopener noreferrer" :aria-label="link.label" class="social">
              <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path :d="link.icon" /></svg>
            </a>
          </li>
        </ul>
      </div>

      <div class="hero__visual">
        <button type="button" class="avatar" :aria-label="t('hero.openPhoto')" @click="openPreview">
          <span class="avatar__ring"></span>
          <img :src="avatar" :alt="t('hero.name')" class="avatar__img" />
        </button>
        <div class="orbit" aria-hidden="true">
          <span v-for="(tag, i) in orbitTags" :key="tag" class="orbit__tag"
            :style="{ '--a': `${(360 / orbitTags.length) * i}deg` }">
            <span class="orbit__label">{{ tag }}</span>
          </span>
        </div>
      </div>
    </div>

    <a href="#about" class="scroll-hint" :aria-label="t('hero.scroll')" @click.prevent="scrollToSection('about')">
      <span class="scroll-hint__line"></span>
      <span class="font-mono">scroll</span>
    </a>
  </section>

  <Teleport to="body">
    <Transition name="zoom">
      <div v-if="isPreviewOpen" class="preview" @click="closePreview">
        <button type="button" class="preview__close" :aria-label="t('hero.closePhoto')" @click="closePreview">
          <span class="mdi mdi-close"></span>
        </button>
        <img :src="avatar" :alt="t('hero.name')" class="preview__img" @click.stop />
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import avatar from '@/assets/img/avatar.png'
import SignalNetwork from '@/components/landing/effects/SignalNetwork.vue'
import { socials } from '@/common/constants/socials'

const sectionId = 'hero'
const cv = '/files/cv_asemochkin.pdf'
const orbitTags = ['Python', 'FastAPI', 'Vue.js', 'Docker', 'IoT', 'ML']

const { t, tm, rt, locale } = useI18n()

const nameWords = computed(() => t('hero.name').split(' '))

// --- «Терминал» и печатающиеся роли ---
const typedCmd = ref('')
const typedRole = ref('')
const timers = []
let roleIndex = 0
let alive = true

const roles = computed(() => tm('hero.roles').map((r) => rt(r)))

function wait(ms) {
  return new Promise((resolve) => timers.push(setTimeout(resolve, ms)))
}

async function typeInto(target, text, speed = 55) {
  for (let i = 1; i <= text.length && alive; i++) {
    target.value = text.slice(0, i)
    await wait(speed)
  }
}

async function eraseFrom(target, speed = 28) {
  while (target.value.length && alive) {
    target.value = target.value.slice(0, -1)
    await wait(speed)
  }
}

async function runRoles() {
  while (alive) {
    const list = roles.value
    if (!list.length) return
    await typeInto(typedRole, list[roleIndex % list.length], 60)
    await wait(2200)
    await eraseFrom(typedRole)
    await wait(300)
    roleIndex += 1
  }
}

// при смене языка перезапускаем текущую роль сразу
watch(locale, () => {
  typedRole.value = ''
})

// --- Превью фото ---
const isPreviewOpen = ref(false)

function openPreview() {
  isPreviewOpen.value = true
  window.addEventListener('keydown', handleEscape)
}

function closePreview() {
  isPreviewOpen.value = false
  window.removeEventListener('keydown', handleEscape)
}

function handleEscape(event) {
  if (event.key === 'Escape') closePreview()
}

function scrollToSection(anchor) {
  const el = document.getElementById(anchor)
  if (!el) return
  const header = document.querySelector('.site-header')
  const offset = header ? header.offsetHeight : 0
  window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - offset + 1, behavior: 'smooth' })
}

onMounted(async () => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (reduced) {
    typedCmd.value = 'whoami'
    typedRole.value = roles.value[0] || ''
    return
  }
  await wait(200)
  await typeInto(typedCmd, 'whoami', 90)
  await wait(900)
  runRoles()
})

onBeforeUnmount(() => {
  alive = false
  timers.forEach(clearTimeout)
  window.removeEventListener('keydown', handleEscape)
})
</script>

<style scoped>
.hero {
  position: relative;
  display: flex;
  align-items: center;
  min-height: 100svh;
  padding-block: 7rem 5rem;
  isolation: isolate;
}

.hero__inner {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(0, 0.75fr);
  align-items: center;
  gap: clamp(2rem, 6vw, 5rem);
}

.terminal {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 1.5rem;
  padding: 0.45rem 0.9rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: rgb(255 255 255 / 0.03);
  font-size: 0.85rem;
  color: var(--muted);
  min-height: 2.1rem;
}

.terminal__prompt {
  color: var(--accent-3);
}

.terminal__cmd {
  color: var(--text);
}

.terminal__caret {
  width: 0.5rem;
  height: 1rem;
  margin-left: -0.35rem;
  background: var(--accent);
  animation: blink 1s steps(1) infinite;
}

@keyframes blink {
  50% { opacity: 0; }
}

.hero__name {
  display: flex;
  flex-wrap: wrap;
  gap: 0 0.3em;
  font-size: clamp(2.6rem, 8.2vw, 6.4rem);
  font-weight: 700;
  line-height: 0.98;
  letter-spacing: -0.04em;
}

.hero__word {
  display: inline-flex;
  overflow: hidden;
  padding-bottom: 0.08em;
}

.hero__word.text-gradient {
  animation: none;
}

/* градиент «растянут» на всё слово: каждая буква показывает свой кусок */
.hero__word.text-gradient .hero__char {
  background: var(--grad);
  background-size: calc(var(--n) * 100%) 100%;
  background-position: calc(var(--i) / max(var(--n) - 1, 1) * 100%) 0;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.hero__char {
  display: inline-block;
  transform: translateY(110%) rotate(8deg);
  opacity: 0;
  animation: char-rise 1s var(--ease-out) forwards;
  animation-delay: var(--d);
}

@keyframes char-rise {
  to {
    transform: none;
    opacity: 1;
  }
}

.hero__role {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  min-height: 2.2rem;
  margin-top: 1.3rem;
  font-size: clamp(1rem, 2.2vw, 1.35rem);
  color: var(--accent);
}

.hero__role-bracket {
  color: var(--muted);
}

.hero__role-caret {
  margin-left: -0.2rem;
  color: var(--accent-2);
  animation: blink 0.9s steps(1) infinite;
}

.hero__about {
  max-width: 36rem;
  margin-top: 1.25rem;
  font-size: 1.08rem;
  line-height: 1.75;
  color: var(--muted);
  opacity: 0;
  animation: fade-up 1s var(--ease-out) 1.1s forwards;
}

.hero__cta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.9rem;
  margin-top: 2.2rem;
  opacity: 0;
  animation: fade-up 1s var(--ease-out) 1.3s forwards;
}

.hero__socials {
  display: flex;
  gap: 0.6rem;
  margin-top: 2rem;
  padding: 0;
  list-style: none;
  opacity: 0;
  animation: fade-up 1s var(--ease-out) 1.5s forwards;
}

.social {
  display: grid;
  place-items: center;
  width: 2.75rem;
  height: 2.75rem;
  border: 1px solid var(--line);
  border-radius: 50%;
  color: var(--muted);
  transition: color 0.3s ease, border-color 0.3s ease, transform 0.4s var(--ease-out), background-color 0.3s ease;
}

.social svg {
  width: 1.15rem;
  height: 1.15rem;
}

.social:hover {
  color: var(--accent);
  border-color: var(--accent);
  background: rgb(34 211 238 / 0.08);
  transform: translateY(-3px) rotate(-6deg);
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: none; }
}

/* --- Аватар с вращающимся градиентным кольцом и орбитой --- */
.hero__visual {
  position: relative;
  display: grid;
  place-items: center;
  aspect-ratio: 1;
  width: min(100%, 440px);
  justify-self: center;
  container-type: inline-size;
  opacity: 0;
  animation: visual-in 1.4s var(--ease-out) 0.4s forwards;
}

@keyframes visual-in {
  from { opacity: 0; transform: scale(0.85) rotate(-8deg); }
  to { opacity: 1; transform: none; }
}

.avatar {
  position: relative;
  width: 64%;
  aspect-ratio: 1;
  border-radius: 50%;
  cursor: zoom-in;
  transition: transform 0.6s var(--ease-out);
}

.avatar:hover {
  transform: scale(1.04);
}

.avatar__ring {
  position: absolute;
  inset: -6px;
  border-radius: 50%;
  background: conic-gradient(from 0deg, var(--accent), var(--accent-2), #f472b6, var(--accent-3), var(--accent));
  animation: spin 6s linear infinite;
  filter: blur(0.5px);
}

.avatar__ring::after {
  content: "";
  position: absolute;
  inset: -18px;
  border-radius: 50%;
  background: inherit;
  filter: blur(34px);
  opacity: 0.45;
}

.avatar__img {
  position: relative;
  width: 100%;
  height: 100%;
  border: 5px solid var(--bg);
  border-radius: 50%;
  object-fit: cover;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.orbit {
  position: absolute;
  inset: 0;
  border: 1px dashed rgb(255 255 255 / 0.1);
  border-radius: 50%;
  animation: spin 40s linear infinite;
  pointer-events: none;
}

.orbit__tag {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  /* точка на окружности орбиты, без собственного поворота */
  transform: rotate(var(--a)) translateY(-50cqw) rotate(calc(-1 * var(--a)));
}

.orbit__label {
  position: absolute;
  top: 0;
  left: 0;
  translate: -50% -50%;
  padding: 0.3rem 0.7rem;
  border: 1px solid var(--line-strong);
  border-radius: 999px;
  background: rgb(10 12 18 / 0.85);
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text);
  white-space: nowrap;
  /* вращаемся навстречу орбите — подпись остаётся горизонтальной */
  animation: counter-spin 40s linear infinite;
}

@keyframes counter-spin {
  from { rotate: 0deg; }
  to { rotate: -360deg; }
}

/* --- Подсказка скролла --- */
.scroll-hint {
  position: absolute;
  left: 50%;
  bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.7rem;
  letter-spacing: 0.2em;
  color: var(--muted);
  transform: translateX(-50%);
}

.scroll-hint__line {
  position: relative;
  width: 1px;
  height: 3rem;
  overflow: hidden;
  background: var(--line);
}

.scroll-hint__line::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(transparent, var(--accent));
  animation: drip 2s var(--ease-out) infinite;
}

@keyframes drip {
  from { transform: translateY(-100%); }
  to { transform: translateY(100%); }
}

/* --- Превью фото --- */
.preview {
  position: fixed;
  inset: 0;
  z-index: 90;
  display: grid;
  place-items: center;
  padding: 1.5rem;
  background: rgb(0 0 0 / 0.8);
  backdrop-filter: blur(10px);
}

.preview__img {
  max-height: 70vh;
  max-width: min(92vw, 720px);
  border: 1px solid var(--line-strong);
  border-radius: 2rem;
  object-fit: contain;
}

.preview__close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 2rem;
  color: rgb(255 255 255 / 0.8);
}

.zoom-enter-active,
.zoom-leave-active {
  transition: opacity 0.35s ease;
}

.zoom-enter-active .preview__img,
.zoom-leave-active .preview__img {
  transition: transform 0.5s var(--ease-out);
}

.zoom-enter-from,
.zoom-leave-to {
  opacity: 0;
}

.zoom-enter-from .preview__img,
.zoom-leave-to .preview__img {
  transform: scale(0.85);
}

@media (max-width: 900px) {
  .hero__inner {
    grid-template-columns: 1fr;
  }

  .hero__visual {
    order: -1;
    width: min(72vw, 300px);
  }

  .orbit__label {
    font-size: 0.62rem;
  }
}
</style>
