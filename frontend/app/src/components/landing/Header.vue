<template>
  <header class="site-header" :class="{ 'is-scrolled': scrolled }">
    <nav class="nav shell">
      <a href="#hero" class="brand" @click.prevent="scrollToSection('hero')">
        <span class="brand__prompt">~/</span>aledev<span class="brand__caret" aria-hidden="true"></span>
      </a>

      <div class="nav__links">
        <a v-for="item in menu" :key="item.key" :href="`#${item.anchor}`" class="nav__link"
          :class="{ 'is-active': activeSection === item.anchor }" @click.prevent="scrollToSection(item.anchor)">
          {{ t(`header.menu.${item.key}`) }}
        </a>
      </div>

      <div class="nav__actions">
        <a :href="resumeUrl" class="resume" :title="t('header.resumeTitle')" :aria-label="t('header.resumeTitle')" download>
          <Icon :path="mdiFileDownloadOutline" class="resume__icon" />
          <span class="resume__label">{{ t('header.resume') }}</span>
        </a>

        <div class="lang" role="group" aria-label="Language">
          <button v-for="lang in langs" :key="lang" type="button" class="lang__btn"
            :class="{ 'is-active': locale === lang }" :aria-pressed="locale === lang" @click="changeLang(lang)">
            {{ lang.toUpperCase() }}
          </button>
          <span class="lang__thumb" :style="{ transform: `translateX(${langs.indexOf(locale) * 100}%)` }"></span>
        </div>


        <button type="button" class="burger" :class="{ 'is-open': mobileOpen }" :aria-expanded="mobileOpen"
          aria-label="Menu" @click="mobileOpen = !mobileOpen">
          <span></span><span></span>
        </button>
      </div>
    </nav>

    <Transition name="drawer">
      <div v-if="mobileOpen" class="drawer">
        <a v-for="(item, i) in menu" :key="item.key" :href="`#${item.anchor}`" class="drawer__link"
          :style="{ '--i': i }" @click.prevent="scrollToSection(item.anchor)">
          <span class="drawer__num">0{{ i + 1 }}</span>
          {{ t(`header.menu.${item.key}`) }}
        </a>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import Icon from '@/components/ui/Icon.vue'
import { mdiArrowTopRight, mdiFileDownloadOutline } from '@mdi/js'
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

const langs = ['ru', 'en']
const resumeUrl = computed(() => `${import.meta.env.VITE_PORTFOLIO_URL || ""}/api/v1/export/portfolio/?lang=${locale.value}`)
const menu = [
  { key: 'about', anchor: 'about' },
  { key: 'projects', anchor: 'projects' },
  { key: 'mentoring', anchor: 'mentoring' },
  { key: 'experience', anchor: 'experience' },
  { key: 'contacts', anchor: 'contacts' },
]

const scrolled = ref(false)
const mobileOpen = ref(false)
const activeSection = ref('')
let spy = null

function changeLang(lang) {
  locale.value = lang
  try {
    localStorage.setItem('locale', lang)
  } catch {
    // хранилище недоступно - язык просто не запомнится
  }
}

watch(locale, (lang) => {
  document.documentElement.lang = lang
}, { immediate: true })

watch(mobileOpen, (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
})

function scrollToSection(anchor) {
  mobileOpen.value = false
  const el = document.getElementById(anchor)
  if (!el) return
  const header = document.querySelector('.site-header')
  const offset = header ? header.offsetHeight : 0
  const sectionPadding = el.classList.contains('section')
    ? Number.parseFloat(getComputedStyle(el).paddingTop) || 0
    : 0
  const gap = el.classList.contains('section') ? 24 : 0
  window.scrollTo({
    top: el.getBoundingClientRect().top + window.scrollY + sectionPadding - offset - gap + 1,
    behavior: 'smooth',
  })
}

function onScroll() {
  scrolled.value = window.scrollY > 24
}

onMounted(() => {
  try {
    const saved = localStorage.getItem('locale')
    if (saved && langs.includes(saved)) locale.value = saved
  } catch {
    // игнорируем
  }

  onScroll()
  window.addEventListener('scroll', onScroll, { passive: true })

  spy = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) activeSection.value = entry.target.id
    }
  }, { rootMargin: '-45% 0px -50% 0px' })

  // секции подгружаются асинхронно - ждём один кадр
  requestAnimationFrame(() => {
    for (const item of menu) {
      const el = document.getElementById(item.anchor)
      if (el) spy.observe(el)
    }
  })
})

onBeforeUnmount(() => {
  spy?.disconnect()
  window.removeEventListener('scroll', onScroll)
  document.body.style.overflow = ''
})
</script>

<style scoped>
.site-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  padding-top: 1rem;
  transition: padding 0.4s var(--ease-out);
}

.site-header.is-scrolled {
  padding-top: 0.6rem;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.55rem 0.6rem 0.55rem 1.25rem;
  border: 1px solid transparent;
  border-radius: 999px;
  transition: background-color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
}

.is-scrolled .nav {
  border-color: var(--line);
  background: rgb(var(--panel-rgb) / 0.72);
  backdrop-filter: blur(18px) saturate(1.4);
  box-shadow: 0 10px 40px -20px rgb(0 0 0 / 0.8);
}

.brand {
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: -0.01em;
  white-space: nowrap;
}

.brand__prompt {
  color: var(--accent);
}

/* Курсор терминала - горит ровно, без мигания */
.brand__caret {
  display: inline-block;
  width: 0.55em;
  height: 1.05em;
  margin-left: 0.15em;
  vertical-align: -0.15em;
  background: var(--accent);
  box-shadow: 0 0 10px rgb(var(--accent-rgb) / 0.45);
}

.nav__links {
  display: flex;
  gap: 0.25rem;
}

.nav__link {
  position: relative;
  padding: 0.5rem 0.9rem;
  border-radius: 999px;
  color: var(--muted);
  font-size: 0.92rem;
  font-weight: 600;
  transition: color 0.3s ease, background-color 0.3s ease;
}

.nav__link:hover {
  color: var(--text);
}

.nav__link.is-active {
  color: var(--text);
  background: var(--surface-2);
}

.nav__link.is-active::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: 0.2rem;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent);
  transform: translateX(-50%);
}

.nav__actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.resume {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  height: 2.5rem;
  padding: 0 0.9rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  color: var(--muted);
  font-size: 0.82rem;
  font-weight: 600;
  transition: color 0.2s ease, border-color 0.2s ease, background-color 0.2s ease;
}

.resume:hover,
.resume:focus-visible {
  border-color: var(--accent);
  background: rgb(var(--accent-rgb) / 0.08);
  color: var(--text);
}

.resume__icon {
  width: 1.1rem;
  height: 1.1rem;
}

.lang {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 3px;
  border: 1px solid var(--line);
  border-radius: 999px;
}

.lang__btn {
  position: relative;
  z-index: 1;
  width: 2.6rem;
  padding: 0.5rem 0;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--muted);
  transition: color 0.3s ease;
}

.lang__btn.is-active {
  color: var(--on-accent);
}

.lang__thumb {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 2.6rem;
  height: calc(100% - 6px);
  border-radius: 999px;
  background: var(--accent);
  transition: transform 0.45s var(--ease-out);
}

.burger {
  display: none;
  position: relative;
  width: 2.6rem;
  height: 2.6rem;
  border: 1px solid var(--line-strong);
  border-radius: 50%;
}

.burger span {
  position: absolute;
  left: 50%;
  width: 1rem;
  height: 1.5px;
  background: var(--text);
  transition: transform 0.4s var(--ease-out);
}

.burger span:first-child { transform: translate(-50%, -3px); }
.burger span:last-child { transform: translate(-50%, 3px); }
.burger.is-open span:first-child { transform: translate(-50%, 0) rotate(45deg); }
.burger.is-open span:last-child { transform: translate(-50%, 0) rotate(-45deg); }

.drawer {
  position: fixed;
  inset: 0;
  z-index: -1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.5rem;
  padding: 6rem 1.5rem 2rem;
  background: rgb(var(--bg-rgb) / 0.96);
  backdrop-filter: blur(20px);
}

.drawer__link {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  padding: 0.6rem 0;
  border-bottom: 1px solid var(--line);
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 8vw, 2.6rem);
  font-weight: 600;
  animation: drawer-in 0.7s var(--ease-out) both;
  animation-delay: calc(var(--i) * 70ms + 80ms);
}

.drawer__num {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--accent);
}

@keyframes drawer-in {
  from { opacity: 0; transform: translateY(24px); }
}

.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.4s ease, clip-path 0.6s var(--ease-out);
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
  clip-path: circle(0% at calc(100% - 2.5rem) 2.5rem);
}

.drawer-enter-to,
.drawer-leave-from {
  clip-path: circle(150% at calc(100% - 2.5rem) 2.5rem);
}

@media (max-width: 860px) {
  .nav__links {
    display: none;
  }

  .resume {
    width: 2.5rem;
    padding: 0;
    justify-content: center;
  }

  .resume__label {
    display: none;
  }

  .burger {
    display: block;
  }
}
</style>
