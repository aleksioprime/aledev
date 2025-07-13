<template>
  <section :id="sectionId" class="container mx-auto py-12">
    <h2 class="text-2xl md:text-3xl font-bold mb-8 text-center">
      {{ $t('projects.sectionTitle') }}
    </h2>
    <div class="grid gap-6 md:grid-cols-2">
      <div v-for="proj in projects" :key="proj.title"
        class="pa-5 flex flex-col bg-neutral-800 rounded-2xl shadow-lg p-6 hover:shadow-2xl transition group animate-fade-in-up">
        <h3 class="text-xl font-semibold mb-2 group-hover:text-cyan-400 transition">{{ proj.title }}</h3>
        <div class="text-cyan-300 mb-1 text-sm">{{ proj.stack }}</div>
        <p class="text-neutral-300 mb-4">{{ proj.desc }}</p>
        <div class="flex gap-4 mt-auto">
          <a v-if="proj.github" :href="proj.github" target="_blank" class="underline hover:text-cyan-400 transition">
            {{ $t('projects.github') }}
          </a>
          <a v-if="proj.demo" :href="proj.demo" target="_blank" class="underline hover:text-cyan-400 transition">
            {{ $t('projects.demo') }}
          </a>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue"
const sectionId = "projects"
const projects = ref([
  {
    title: "Hyperspectrus",
    stack: "FastAPI, Vue.js, Celery, PostgreSQL, PyQT, OpenCV",
    desc: "Платформа для анализа гиперспектральных данных. Архитектура на микросервисах, автоматизация пайплайнов.",
    github: "https://github.com/aleksioprime/hyperspectrus",
    demo: "#"
  },
  {
    title: "EmPolimer",
    stack: "FastAPI, Vue.js, MQTT, Arduino",
    desc: "Устройство снятия показаний с датчиков в биоустановке и платформа c MQTT-сервисом для мониторинга данных микроклимата",
    github: "https://github.com/aleksioprime/sk-empolimer",
    demo: "#"
  }
])
</script>

<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(40px);
  }

  to {
    opacity: 1;
    transform: none;
  }
}

.animate-fade-in-up {
  animation: fade-in-up 1s cubic-bezier(.22, .68, .4, 1) both;
}
</style>