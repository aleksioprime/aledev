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
import { getBaseTitleByRoute } from "@/utils/siteConfig";

import { useRoute } from 'vue-router'
const route = useRoute()

watch(
  () => [route.name, route.query],
  () => {
    const baseTitle = getBaseTitleByRoute(route);

    document.title = route.meta.title
      ? `${baseTitle} — ${route.meta.title}`
      : baseTitle;
  },
  { immediate: true }
)
</script>

<style scoped></style>
