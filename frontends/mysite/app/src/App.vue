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
import { getCurrentDomain, DOMAINS, getDomainConfig } from "@/utils/domainUtils";

import { useRoute } from 'vue-router'
const route = useRoute()

watch(
  () => [route.name, route.query],
  () => {
    const domainConfig = getDomainConfig();
    const baseTitle = domainConfig.title;

    document.title = route.meta.title
      ? `${baseTitle} — ${route.meta.title}`
      : baseTitle;
  },
  { immediate: true }
)
</script>

<style scoped></style>