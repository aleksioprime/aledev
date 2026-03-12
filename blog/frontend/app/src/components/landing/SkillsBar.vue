<template>
  <section class="container mx-auto py-4">
    <div class="mx-auto flex flex-wrap justify-center gap-3 animate-fade-in" style="max-width: 800px;">
      <span v-for="skill in skills" :key="skill"
            class="bg-neutral-800 text-cyan-200 px-4 py-2 rounded-xl text-base font-medium shadow hover:scale-105 transition cursor-default">
        {{ skill }}
      </span>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue"
const skills = ref([
  "Python", "AsyncIO", "FastAPI", "Django", "Flask", "RabbitMQ", "PostgreSQL", "ETL",
  "JavaScript", "Vue.js", "Docker", "CI/CD", "OpenCV", "TensorFlow", "IoT"
])
</script>
