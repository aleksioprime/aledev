<template>
  <section :id="sectionId" class="container mx-auto pt-16">
    <h2 class="text-2xl md:text-3xl font-bold mb-8 text-center">
      {{ $t('projects.sectionTitle') }}
    </h2>
    <div class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="proj in projects" :key="proj.id || proj.title"
        class="pa-5 flex flex-col bg-neutral-800 rounded-2xl shadow-lg p-6 hover:shadow-2xl transition group animate-fade-in-up">
        <h3 class="text-xl font-semibold mb-2">
          {{ getTranslation(proj, $i18n.locale).title }}
        </h3>
        <div class="text-cyan-300 mb-1 text-sm">{{ proj.stack }}</div>
        <p class="text-neutral-300 mb-4">
          {{ getTranslation(proj, $i18n.locale).description }}
        </p>
        <div class="flex gap-4 mt-auto">
          <a v-if="proj.github_url" :href="proj.github_url" target="_blank"
            class="underline hover:text-cyan-400 transition">
            {{ $t('projects.github') }}
          </a>
          <a v-if="proj.demo_url" :href="proj.demo_url" target="_blank"
            class="underline hover:text-cyan-400 transition">
            {{ $t('projects.demo') }}
          </a>
        </div>
      </div>
    </div>
    <div class="flex justify-center mt-8">
      <button v-if="hasNextPage && !loading" @click="fetchProjects()"
        class="px-6 py-2 !bg-cyan-700 rounded-xl text-white font-bold hover:!bg-cyan-800 transition">
        {{ $t('projects.showMore') }}
      </button>
      <span v-if="loading"
        class="w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin"></span>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";

import { useProjectStore } from "@/stores/project";
const projectStore = useProjectStore();
const projects = ref([]);

const sectionId = "projects";

// --- СПИСОК ПРОЕКТОВ ---

// Переменные пагинированного списка
const page = ref(1);
const limit = 3;
const total = ref(0);
const hasNextPage = ref(true);

// Переменная процесса загрузки
const loading = ref(false);

function getTranslation(proj, currentLang) {
  return proj.translations?.find(t => t.lang === currentLang) ||
    proj.translations?.[0] ||
    { title: proj.title, description: "" };
}

const fetchProjects = async (reset = false) => {
  if (loading.value) return;
  loading.value = true;

  // Если нужно перезагрузить список (например, при смене фильтра)
  if (reset) {
    projects.value = [];
    page.value = 1;
    hasNextPage.value = true;
  }

  // Фильтр "только избранные"
  const params = {
    offset: page.value, // offset обычно = page * limit
    limit,
    is_favorite: true,
  };

  const data = await projectStore.loadProjects({ params });

  if (data) {
    // Если сброс — просто присваиваем, иначе пушим к существующим
    if (reset) {
      projects.value = data.items;
    } else {
      projects.value.push(...data.items);
    }
    total.value = data.total;
    hasNextPage.value = data.has_next;
    page.value += 1;
  } else {
    hasNextPage.value = false;
  }

  loading.value = false;
};

onMounted(() => fetchProjects(true));
</script>

<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(40px);
  }

  to {
    opacity: 1;
    transform: none;
  }
}

.animate-fade-in-up {
  animation: fade-in-up 1s cubic-bezier(.22, .68, .4, 1) both;
}
</style>