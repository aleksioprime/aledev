<template>
  <section :id="sectionId" class="!pt-12 pb-4 text-center flex flex-col items-center animate-fade-in">
    <img :src="avatar" alt="avatar"
      class="w-28 h-28 rounded-full mb-5 shadow-lg border-2 border-neutral-800 object-cover" />
    <h1 class="text-3xl md:text-5xl font-extrabold mb-2 tracking-tight">{{ t('hero.name') }}</h1>
    <h2 class="text-xl md:text-2xl text-cyan-400 mb-3 font-semibold">{{ t('hero.title') }}</h2>
    <p class="max-w-xl text-neutral-400 mb-6">{{ t('hero.about') }}</p>
    <div class="flex gap-4 justify-center mb-4">
      <a :href="cv"
        class="px-5 py-2 rounded-full border border-cyan-400 text-cyan-400 hover:bg-cyan-400 hover:text-neutral-900 font-medium transition"
        target="_blank">
        {{ t('hero.download_cv') }}
      </a>
      <a href="javascript:void(0)" @click="scrollToSection('contacts')"
        class="px-5 py-2 rounded-full border border-neutral-700 text-neutral-200 hover:bg-neutral-800 font-medium transition">
        {{ t('hero.contact') }}
      </a>
    </div>
    <div class="flex gap-4 justify-center mt-2 text-2xl">
      <a v-for="link in socials" :key="link.href" :href="link.href" target="_blank"
        class="hover:text-cyan-400 transition">
        <i :class="link.icon"></i>
      </a>
    </div>
  </section>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import avatar from "@/assets/img/avatar.png"

const sectionId = "about"
const cv = "/cv.pdf"
const socials = [
  { icon: "fa-brands fa-github", href: "https://github.com/your-github" },
  { icon: "fa-brands fa-linkedin", href: "https://linkedin.com/in/your-linkedin" },
  { icon: "fa-brands fa-telegram", href: "https://t.me/your-telegram" }
]

const { t } = useI18n()

function scrollToSection(anchor) {
  const el = document.getElementById(anchor)
  if (el) el.scrollIntoView({ behavior: "smooth" })
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(30px);
  }

  to {
    opacity: 1;
    transform: none;
  }
}

.animate-fade-in {
  animation: fade-in 1s cubic-bezier(.2, .8, .4, 1) both;
}
</style>