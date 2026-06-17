<template>
  <section :id="sectionId" class="container mx-auto pt-16">
    <div class="mb-8 flex items-center justify-between gap-4">
      <h2 class="text-2xl md:text-3xl font-bold">
        {{ $t('projects.sectionTitle') }}
      </h2>

      <div class="hidden sm:flex items-center gap-2">
        <button type="button" class="carousel-control" :aria-label="$t('projects.previous')" @click="scrollCarousel(-1)">
          <span class="mdi mdi-chevron-left"></span>
        </button>
        <button type="button" class="carousel-control" :aria-label="$t('projects.next')" @click="scrollCarousel(1)">
          <span class="mdi mdi-chevron-right"></span>
        </button>
      </div>
    </div>

    <div class="relative">
      <div ref="carouselRef" class="projects-carousel">
        <button v-for="proj in projects" :key="proj.id || getProjectTitle(proj)" type="button" class="project-card group"
          :aria-label="`${$t('projects.openDetails')}: ${getProjectTitle(proj)}`" @click="openProject(proj)">
          <div class="mb-5 flex items-start justify-between gap-4">
            <h3 class="text-xl font-semibold leading-tight">
              {{ getProjectTitle(proj) }}
            </h3>
            <span class="mdi mdi-arrow-top-right text-cyan-300 transition group-hover:translate-x-1 group-hover:-translate-y-1"></span>
          </div>

          <div v-if="proj.stack" class="mb-4 flex flex-wrap gap-2">
            <span v-for="item in getStackItems(proj.stack)" :key="item" class="stack-chip">
              {{ item }}
            </span>
          </div>

          <p class="line-clamp-4 text-left text-sm leading-6 text-neutral-300">
            {{ getProjectSummary(proj) }}
          </p>

          <span class="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-cyan-300">
            {{ $t('projects.details') }}
            <span class="mdi mdi-chevron-right text-base"></span>
          </span>
        </button>
      </div>

      <div class="pointer-events-none absolute inset-y-0 left-0 hidden w-12 bg-gradient-to-r from-neutral-950 to-transparent md:block"></div>
      <div class="pointer-events-none absolute inset-y-0 right-0 hidden w-12 bg-gradient-to-l from-neutral-950 to-transparent md:block"></div>
    </div>

    <div class="mt-8 flex justify-center">
      <button v-if="hasNextPage && !loading" type="button" @click="fetchProjects()"
        class="rounded-xl !bg-cyan-700 px-6 py-2 font-bold text-white transition hover:!bg-cyan-800">
        {{ $t('projects.showMore') }}
      </button>
      <span v-if="loading" class="h-4 w-4 animate-spin rounded-full border-2 border-cyan-400 border-t-transparent"></span>
    </div>

    <Teleport to="body">
      <div v-if="selectedProject" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
        @click.self="closeProject">
        <article class="project-modal">
          <div class="mb-5 flex items-start justify-between gap-4">
            <div>
              <p v-if="selectedProject.stack" class="mb-2 text-sm font-semibold uppercase tracking-wide text-cyan-300">
                {{ $t('projects.stack') }}
              </p>
              <h3 class="text-2xl font-bold leading-tight md:text-3xl">
                {{ getProjectTitle(selectedProject) }}
              </h3>
            </div>
            <button type="button" class="modal-close" :aria-label="$t('projects.close')" @click="closeProject">
              <span class="mdi mdi-close"></span>
            </button>
          </div>

          <div v-if="selectedProject.stack" class="mb-6 flex flex-wrap gap-2">
            <span v-for="item in getStackItems(selectedProject.stack)" :key="item" class="stack-chip">
              {{ item }}
            </span>
          </div>

          <p class="whitespace-pre-line text-base leading-7 text-neutral-200">
            {{ getProjectDescription(selectedProject) }}
          </p>

          <div v-if="selectedProject.github_url || selectedProject.demo_url || selectedProject.link"
            class="mt-8 flex flex-wrap gap-3">
            <a v-if="selectedProject.github_url" :href="selectedProject.github_url" target="_blank" rel="noopener noreferrer"
              class="project-link">
              <span class="mdi mdi-github"></span>
              {{ $t('projects.github') }}
            </a>
            <a v-if="selectedProject.demo_url" :href="selectedProject.demo_url" target="_blank" rel="noopener noreferrer"
              class="project-link">
              <span class="mdi mdi-open-in-new"></span>
              {{ $t('projects.demo') }}
            </a>
            <a v-if="selectedProject.link" :href="selectedProject.link" target="_blank" rel="noopener noreferrer"
              class="project-link">
              <span class="mdi mdi-link-variant"></span>
              {{ $t('projects.links') }}
            </a>
          </div>
        </article>
      </div>
    </Teleport>
  </section>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useI18n } from "vue-i18n";

import { useProjectStore } from "@/stores/project";

const projectStore = useProjectStore();
const { locale } = useI18n();
const projects = ref([]);
const carouselRef = ref(null);
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

function scrollCarousel(direction) {
  const carousel = carouselRef.value;
  if (!carousel) return;

  const card = carousel.querySelector(".project-card");
  const distance = card ? card.clientWidth + 24 : carousel.clientWidth * 0.8;
  carousel.scrollBy({ left: direction * distance, behavior: "smooth" });
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
.projects-carousel {
  display: grid;
  grid-auto-columns: minmax(280px, 34%);
  grid-auto-flow: column;
  gap: 1.5rem;
  margin-inline: -1rem;
  overflow-x: auto;
  padding: 0.25rem 1rem 1rem;
  scroll-padding-inline: 1rem;
  scroll-snap-type: x mandatory;
  scrollbar-color: rgb(34 211 238 / 0.7) rgb(38 38 38);
  scrollbar-width: thin;
}

.projects-carousel::-webkit-scrollbar {
  height: 0.6rem;
}

.projects-carousel::-webkit-scrollbar-track {
  background: rgb(38 38 38);
  border-radius: 999px;
}

.projects-carousel::-webkit-scrollbar-thumb {
  background: linear-gradient(90deg, rgb(34 211 238), rgb(45 212 191));
  border-radius: 999px;
}

.project-card {
  min-height: 21rem;
  scroll-snap-align: start;
  border: 1px solid rgb(64 64 64);
  border-radius: 1rem;
  background: linear-gradient(145deg, rgb(38 38 38), rgb(23 23 23));
  box-shadow: 0 20px 60px rgb(0 0 0 / 0.18);
  padding: 1.5rem;
  text-align: left;
  transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease;
}

.project-card:hover {
  border-color: rgb(34 211 238 / 0.65);
  box-shadow: 0 24px 70px rgb(8 145 178 / 0.16);
  transform: translateY(-4px);
}

.carousel-control,
.modal-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border: 1px solid rgb(64 64 64);
  border-radius: 999px;
  background: rgb(38 38 38);
  color: white;
  transition: border-color 180ms ease, background-color 180ms ease, color 180ms ease;
}

.carousel-control:hover,
.modal-close:hover {
  border-color: rgb(34 211 238);
  background: rgb(8 145 178 / 0.2);
  color: rgb(103 232 249);
}

.stack-chip {
  border: 1px solid rgb(34 211 238 / 0.3);
  border-radius: 999px;
  background: rgb(8 145 178 / 0.12);
  padding: 0.25rem 0.65rem;
  font-size: 0.75rem;
  line-height: 1rem;
  color: rgb(165 243 252);
}

.project-modal {
  max-height: min(82vh, 760px);
  width: min(100%, 760px);
  overflow-y: auto;
  border: 1px solid rgb(64 64 64);
  border-radius: 1rem;
  background: rgb(23 23 23);
  box-shadow: 0 24px 90px rgb(0 0 0 / 0.45);
  padding: clamp(1.25rem, 4vw, 2rem);
}

.project-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  border-radius: 999px;
  background: rgb(8 145 178);
  padding: 0.65rem 1rem;
  font-weight: 700;
  color: white;
  transition: background-color 180ms ease;
}

.project-link:hover {
  background: rgb(14 116 144);
}

@media (max-width: 768px) {
  .projects-carousel {
    grid-auto-columns: minmax(82vw, 1fr);
  }
}
</style>
