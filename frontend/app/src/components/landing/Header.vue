<template>
  <header class="sticky top-0 z-50 bg-neutral-950/90 backdrop-blur border-b border-neutral-800">
    <nav class="container mx-auto flex justify-between items-center py-4 px-2 md:px-0">
      <span class="font-bold text-lg tracking-tight">{{ t('header.brand') }}</span>
      <div class="flex align-center gap-3 text-neutral-300">
        <div class="flex align-center">
          <a v-for="item in menu" :key="item.key" href="javascript:void(0)" @click="scrollToSection(item.anchor)"
            class="hover:text-cyan-400 transition-colors px-2 py-1 rounded cursor-pointer">
            {{ t(`header.menu.${item.key}`) }}
          </a>
        </div>
        <!-- Языковой переключатель -->
        <div class="relative">
          <button @click="showDropdown = !showDropdown"
            class="flex items-center gap-1 px-2 pt-0 rounded border border-neutral-700 text-neutral-300 hover:border-cyan-400 hover:text-cyan-400 transition select-none">
            <span v-if="locale.value === 'ru'">🇷🇺</span>
            <span v-if="locale.value === 'en'">🇬🇧</span>
            <span class="ml-1 font-medium">{{ (locale || '').toUpperCase() }}</span>
            <svg class="w-3 h-3 ml-1 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div v-if="showDropdown" @click.away="showDropdown = false"
            class="absolute right-0 mt-2 min-w-[90px] bg-neutral-900 border border-neutral-800 rounded-xl shadow-lg z-50">
            <div v-for="lang in langs" :key="lang" @click="changeLang(lang); showDropdown = false"
              class="flex items-center gap-2 px-3 py-2 cursor-pointer hover:bg-cyan-950/40 transition rounded-xl"
              :class="{ 'font-bold text-cyan-400': locale.value === lang }">
              <span v-if="lang === 'ru'">🇷🇺</span>
              <span v-if="lang === 'en'">🇬🇧</span>
              <span>{{ lang.toUpperCase() }}</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, locale, messages } = useI18n()

const langs = ['ru', 'en']
const showDropdown = ref(false)

function changeLang(lang) {
  locale.value = lang
  console.log('Текущий язык:', locale.value)
  console.log('Доступные сообщения:', messages.value)
}

const menu = [
  { key: "projects", anchor: "projects" },
  { key: "experience", anchor: "experience" },
  { key: "contacts", anchor: "contacts" },
  { key: "cv", anchor: "/files/cv_asemochkin.pdf", ext: true },
]

function scrollToSection(anchor) {
  if (anchor.startsWith('/')) {
    window.open(anchor, '_blank')
    return
  }
  const el = document.getElementById(anchor)
  if (el) {
    const header = document.querySelector('header')
    const headerHeight = header ? header.offsetHeight : 0

    const elementTop = el.getBoundingClientRect().top + window.scrollY

    window.scrollTo({
      top: elementTop - headerHeight + 40,
      behavior: 'smooth'
    })
  }
}
</script>