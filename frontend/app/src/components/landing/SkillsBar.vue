<template>
  <section class="container mx-auto py-4">
    <div class="flex flex-wrap justify-center gap-3 animate-fade-in">
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
  "Python", "AsyncIO", "FastAPI", "Django", "Flask", "RabbitMQ", "Elasticsearch", "PostgreSQL", "ETL",
  "JavaScript", "Vue.js", "Docker", "CI/CD", "OpenCV", "TensorFlow", "IoT"
])
</script>
