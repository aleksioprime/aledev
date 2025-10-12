<template>
  <v-app>
    <app-layout>
      <router-view />
    </app-layout>
  </v-app>
</template>

<script setup>
import { watch } from 'vue'

import AppLayout from "@/layouts/AppLayout.vue";

import { useRoute } from 'vue-router'
const route = useRoute()

watch(
  () => route.name,
  () => {
    document.title = route.meta.title
      ? `Aleksei Semochkin — ${route.meta.title}`
      : 'Aleksei Semochkin — Software Engineer Portfolio';
  },
  { immediate: true }
)
</script>

<style scoped></style>