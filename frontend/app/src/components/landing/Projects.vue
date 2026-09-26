<template>
  <section :id="sectionId" class="section">
    <div class="shell">
      <header class="section-head projects-head">
        <div>
          <span v-reveal class="section-kicker">02 — {{ $t('projects.kicker') }}</span>
          <h2 v-reveal="{ delay: 80 }" class="section-title">{{ $t('projects.sectionTitle') }}</h2>
        </div>
        <p v-reveal="{ delay: 160 }" class="section-lead">{{ $t('projects.lead') }}</p>
      </header>

      <div class="grid">
        <div v-for="(proj, i) in projects" :key="proj.id || getProjectTitle(proj)" v-reveal="{ delay: (i % limit) * 80 }"
          class="grid__cell" :class="{ 'grid__cell--wide': i === 0 }">
          <button v-tilt="5" type="button" class="card"
            :aria-label="`${$t('projects.openDetails')}: ${getProjectTitle(proj)}`" @click="openProject(proj)">
            <ProjectCover :seed="String(proj.id)" :title="getProjectTitle(proj)" class="card__cover" />

            <div class="card__body">
              <span class="card__index font-mono">{{ String(i + 1).padStart(2, '0') }}</span>
              <h3 class="card__title">{{ getProjectTitle(proj) }}</h3>
              <p class="card__summary">{{ getProjectSummary(proj) }}</p>

              <div v-if="proj.stack" class="card__stack">
                <span v-for="item in getStackItems(proj.stack).slice(0, 5)" :key="item" class="chip">{{ item }}</span>
              </div>

              <span class="card__more">
                {{ $t('projects.details') }}
                <span class="card__arrow"><Icon :path="mdiArrowTopRight" /></span>
              </span>
            </div>
          </button>
        </div>

        <!-- Скелетоны при первой загрузке -->
        <template v-if="loading && !projects.length">
          <div v-for="n in 3" :key="`s-${n}`" class="grid__cell" :class="{ 'grid__cell--wide': n === 1 }">
            <div class="card card--skeleton"></div>
          </div>
        </template>
      </div>

      <p v-if="!loading && !projects.length" class="empty font-mono">{{ $t('projects.empty') }}</p>

      <div class="more">
        <button v-if="hasNextPage && !loading && projects.length" v-magnetic type="button" class="btn btn-ghost"
          @click="fetchProjects()">
          {{ $t('projects.showMore') }}
          <Icon :path="mdiPlus" />
        </button>
        <span v-if="loading && projects.length" class="spinner" :aria-label="$t('projects.loading')"></span>
      </div>
    </div>

    <Teleport to="body">
      <Transition name="modal">
        <div v-if="selectedProject" class="overlay" @click.self="closeProject">
          <article class="modal" role="dialog" aria-modal="true" :aria-label="getProjectTitle(selectedProject)">
            <ProjectCover :seed="String(selectedProject.id)" :title="getProjectTitle(selectedProject)"
              class="modal__cover" />

            <button type="button" class="modal__close" :aria-label="$t('projects.close')" @click="closeProject">
              <Icon :path="mdiClose" />
            </button>

            <div class="modal__body">
              <h3 class="modal__title font-display">{{ getProjectTitle(selectedProject) }}</h3>

              <div v-if="selectedProject.stack" class="modal__stack">
                <span class="modal__label font-mono">{{ $t('projects.stack') }}</span>
                <div class="card__stack">
                  <span v-for="item in getStackItems(selectedProject.stack)" :key="item" class="chip">{{ item }}</span>
                </div>
              </div>

              <p class="modal__text">{{ getProjectDescription(selectedProject) }}</p>

              <div v-if="selectedProject.github_url || selectedProject.demo_url || selectedProject.link"
                class="modal__links">
                <a v-if="selectedProject.demo_url" :href="selectedProject.demo_url" target="_blank"
                  rel="noopener noreferrer" class="btn btn-primary">
                  <Icon :path="mdiOpenInNew" />
                  {{ $t('projects.demo') }}
                </a>
                <a v-if="selectedProject.github_url" :href="selectedProject.github_url" target="_blank"
                  rel="noopener noreferrer" class="btn btn-ghost">
                  <Icon :path="mdiGithub" />
                  {{ $t('projects.github') }}
                </a>
                <a v-if="selectedProject.link" :href="selectedProject.link" target="_blank" rel="noopener noreferrer"
                  class="btn btn-ghost">
                  <Icon :path="mdiLinkVariant" />
                  {{ $t('projects.links') }}
                </a>
              </div>
            </div>
          </article>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<script setup>
import Icon from '@/components/ui/Icon.vue'
import { mdiArrowTopRight, mdiClose, mdiGithub, mdiLinkVariant, mdiOpenInNew, mdiPlus } from '@mdi/js'
import { onMounted, onUnmounted, ref } from "vue";
import { useI18n } from "vue-i18n";

import { useProjectStore } from "@/stores/project";
import ProjectCover from "@/components/landing/effects/ProjectCover.vue";

const projectStore = useProjectStore();
const { locale } = useI18n();
const projects = ref([]);
const selectedProject = ref(null);

const sectionId = "projects";

const page = ref(1);
const limit = 8;
const total = ref(0);
const hasNextPage = ref(true);
const loading = ref(false);

function getTranslation(proj, currentLang) {
  return proj.translations?.find(t => t.lang === currentLang) ||
    proj.translations?.find(t => t.lang === "ru") ||
    proj.translations?.[0] ||
    { title: proj.title, short_description: "", description: "" };
}

function getCurrentTranslation(proj) {
  return getTranslation(proj, locale.value);
}

function getProjectTitle(proj) {
  return getCurrentTranslation(proj).title || "";
}

function getProjectSummary(proj) {
  const translation = getCurrentTranslation(proj);
  return translation.short_description || translation.description || "";
}

function getProjectDescription(proj) {
  const translation = getCurrentTranslation(proj);
  return translation.description || translation.short_description || "";
}

function getStackItems(stack) {
  return stack.split(",").map(item => item.trim()).filter(Boolean);
}

function openProject(project) {
  selectedProject.value = project;
  document.body.style.overflow = "hidden";
}

function closeProject() {
  selectedProject.value = null;
  document.body.style.overflow = "";
}

function handleKeydown(event) {
  if (event.key === "Escape" && selectedProject.value) {
    closeProject();
  }
}

const fetchProjects = async (reset = false) => {
  if (loading.value) return;
  loading.value = true;

  if (reset) {
    projects.value = [];
    page.value = 1;
    hasNextPage.value = true;
  }

  const params = {
    offset: page.value,
    limit,
    is_favorite: true,
  };

  const data = await projectStore.loadProjects({ params });

  if (data) {
    projects.value.push(...data.items);
    total.value = data.total;
    hasNextPage.value = data.has_next;
    page.value += 1;
  } else {
    hasNextPage.value = false;
  }

  loading.value = false;
};

onMounted(() => {
  fetchProjects(true);
  window.addEventListener("keydown", handleKeydown);
});

onUnmounted(() => {
  window.removeEventListener("keydown", handleKeydown);
  document.body.style.overflow = "";
});
</script>

<style scoped>
.projects-head {
  flex-direction: row;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1.5rem 3rem;
}

.projects-head > div {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.25rem;
}

.grid__cell--wide {
  grid-column: span 2;
}

.card {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 1.5rem;
  background: var(--bg-2);
  text-align: left;
  transition: transform 0.5s var(--ease-out), border-color 0.4s ease, box-shadow 0.5s ease;
  transform-style: preserve-3d;
}

/* Подсветка, следующая за курсором */
.card::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 2;
  border-radius: inherit;
  padding: 1px;
  background: radial-gradient(420px circle at var(--mx, 50%) var(--my, 50%), rgb(34 211 238 / 0.9), rgb(167 139 250 / 0.4) 35%, transparent 60%);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.card::after {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(600px circle at var(--mx, 50%) var(--my, 50%), rgb(34 211 238 / 0.07), transparent 40%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.card:hover {
  box-shadow: 0 30px 80px -30px rgb(34 211 238 / 0.35);
}

.card:hover::before,
.card:hover::after {
  opacity: 1;
}

.card:hover :deep(.cover__svg),
.card:hover :deep(.cover__img) {
  transform: scale(1.08);
}

.card:hover :deep(.cover__mono) {
  transform: translateY(-6px);
}

.card__cover {
  flex-shrink: 0;
}

.grid__cell--wide .card {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
}

.grid__cell--wide .card__cover {
  aspect-ratio: auto;
  min-height: 100%;
}

.card__body {
  position: relative;
  display: flex;
  flex: 1;
  flex-direction: column;
  padding: 1.5rem 1.5rem 1.4rem;
}

.card__index {
  margin-bottom: 0.9rem;
  font-size: 0.75rem;
  color: var(--accent);
}

.card__title {
  margin-bottom: 0.7rem;
  font-size: 1.3rem;
  font-weight: 700;
  line-height: 1.25;
}

.card__summary {
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  font-size: 0.93rem;
  line-height: 1.65;
  color: var(--muted);
}

.card__stack {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 1.1rem;
}

.card__more {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  margin-top: auto;
  padding-top: 1.4rem;
  font-size: 0.88rem;
  font-weight: 700;
}

.card__arrow {
  display: grid;
  place-items: center;
  width: 1.8rem;
  height: 1.8rem;
  border: 1px solid var(--line-strong);
  border-radius: 50%;
  transition: transform 0.5s var(--ease-out), background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.card:hover .card__arrow {
  transform: rotate(45deg);
  border-color: var(--accent);
  background: var(--accent);
  color: #05060a;
}

.card--skeleton {
  min-height: 24rem;
  background: linear-gradient(100deg, var(--bg-2) 30%, rgb(255 255 255 / 0.05) 50%, var(--bg-2) 70%);
  background-size: 300% 100%;
  animation: shimmer 1.6s linear infinite;
}

@keyframes shimmer {
  from { background-position: 100% 0; }
  to { background-position: 0 0; }
}

.empty {
  padding: 3rem 0;
  text-align: center;
  color: var(--muted);
}

.more {
  display: flex;
  justify-content: center;
  margin-top: 3rem;
}

.spinner {
  width: 1.6rem;
  height: 1.6rem;
  border: 2px solid var(--accent);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* --- Модальное окно --- */
.overlay {
  position: fixed;
  inset: 0;
  z-index: 90;
  display: grid;
  place-items: center;
  padding: 1rem;
  background: rgb(0 0 0 / 0.7);
  backdrop-filter: blur(12px);
}

.modal {
  position: relative;
  width: min(100%, 820px);
  max-height: min(88vh, 900px);
  overflow-y: auto;
  border: 1px solid var(--line-strong);
  border-radius: 1.75rem;
  background: var(--bg-2);
  box-shadow: 0 40px 120px -20px rgb(0 0 0 / 0.8);
}

.modal__cover {
  aspect-ratio: 21 / 8;
}

.modal__close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 3;
  display: grid;
  place-items: center;
  width: 2.6rem;
  height: 2.6rem;
  border: 1px solid var(--line-strong);
  border-radius: 50%;
  background: rgb(10 12 18 / 0.7);
  backdrop-filter: blur(8px);
  font-size: 1.2rem;
  transition: transform 0.4s var(--ease-out), border-color 0.3s ease;
}

.modal__close:hover {
  transform: rotate(90deg);
  border-color: var(--accent);
}

.modal__body {
  padding: clamp(1.5rem, 4vw, 2.5rem);
}

.modal__title {
  font-size: clamp(1.6rem, 4vw, 2.4rem);
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.modal__stack {
  margin-top: 1.5rem;
}

.modal__label {
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent);
}

.modal__stack .card__stack {
  margin-top: 0.6rem;
}

.modal__text {
  margin-top: 1.5rem;
  white-space: pre-line;
  line-height: 1.8;
  color: #c9d0dc;
}

.modal__links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 2rem;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.35s ease;
}

.modal-enter-active .modal,
.modal-leave-active .modal {
  transition: transform 0.55s var(--ease-out), opacity 0.4s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal,
.modal-leave-to .modal {
  opacity: 0;
  transform: translateY(40px) scale(0.96);
}

@media (max-width: 1024px) {
  .grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .grid__cell--wide .card {
    display: flex;
  }

  .grid__cell--wide .card__cover {
    aspect-ratio: 16 / 9;
    min-height: 0;
  }
}

@media (max-width: 640px) {
  .grid {
    grid-template-columns: 1fr;
  }

  .grid__cell--wide {
    grid-column: auto;
  }
}
</style>
