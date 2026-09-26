<template>
  <!-- Иконка MDI в виде inline-SVG: в сборку попадают только используемые иконки -->
  <svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
    <path :d="path" fill="currentColor" />
  </svg>
</template>

<script setup>
defineProps({
  path: { type: String, required: true },
})
</script>

<style scoped>
.icon {
  display: inline-block;
  flex-shrink: 0;
  width: 1.15em;
  height: 1.15em;
  vertical-align: -0.2em;
}
</style>
