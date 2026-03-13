<template>
  <footer class="text-center py-6 text-neutral-500 text-sm border-t border-neutral-800 mt-8">
    {{ t('footer.copyright') }} &nbsp;|&nbsp;
    <a :href="githubUrl" target="_blank" class="underline hover:text-cyan-400">
      {{ t('footer.github') }}
    </a>
  </footer>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const githubUrl = 'https://github.com/aleksioprime'
</script>