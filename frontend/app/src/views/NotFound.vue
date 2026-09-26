<template>
  <section class="landing notfound">
    <p class="notfound__cmd font-mono">$ cd {{ path }}<br /><span>bash: {{ path }}: No such file or directory</span></p>
    <h1 class="glitch font-display" data-text="404">404</h1>
    <p class="notfound__text">Страница не найдена · Page not found</p>
    <router-link v-magnetic to="/" class="btn btn-primary">
      <span class="mdi mdi-arrow-left"></span>
      На главную
    </router-link>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const path = computed(() => route.fullPath)
</script>

<style scoped>
.notfound {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  padding: 2rem 1rem;
  text-align: center;
}

.notfound__cmd {
  max-width: 100%;
  overflow-wrap: anywhere;
  font-size: 0.85rem;
  color: var(--accent-3);
}

.notfound__cmd span {
  color: #f87171;
}

.notfound__text {
  color: var(--muted);
}

.glitch {
  position: relative;
  font-size: clamp(6rem, 24vw, 14rem);
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.05em;
}

.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  inset: 0;
}

.glitch::before {
  color: var(--accent);
  animation: glitch 2.6s infinite steps(1);
  mix-blend-mode: screen;
}

.glitch::after {
  color: var(--accent-2);
  animation: glitch 2.6s infinite steps(1) reverse;
  mix-blend-mode: screen;
}

@keyframes glitch {
  0%, 86%, 100% { clip-path: inset(0 0 100% 0); transform: none; }
  88% { clip-path: inset(20% 0 55% 0); transform: translate(-6px, 2px); }
  91% { clip-path: inset(60% 0 10% 0); transform: translate(6px, -2px); }
  94% { clip-path: inset(40% 0 35% 0); transform: translate(-3px, 0); }
}
</style>
