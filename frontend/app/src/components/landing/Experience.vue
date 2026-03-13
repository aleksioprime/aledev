<template>
  <section :id="sectionId" class="container mx-auto pt-12 px-4">
    <h2 class="text-2xl md:text-3xl font-bold mb-12 text-center tracking-tight">
      {{ $t('experience.sectionTitle') }}
    </h2>
    <ol class="relative border-l border-neutral-700 max-w-2xl mx-auto">
      <li v-for="exp in experiences" :key="exp.id" class="mb-12 ml-6 group last:mb-0">
        <span
          class="absolute -left-3 flex items-center justify-center w-6 h-6 bg-cyan-400 rounded-full ring-8 ring-neutral-950 group-hover:scale-110 transition-transform"></span>
        <h3 class="font-bold text-lg text-cyan-400 mb-0.5 group-hover:text-cyan-300 transition-colors">
          {{ getTranslation(exp, $i18n.locale).position }}
        </h3>
        <div class="text-cyan-200 font-semibold text-sm mb-0.5">
          {{ getTranslation(exp, $i18n.locale).company }}
        </div>
        <time class="block mb-1 text-xs text-neutral-400">
          {{ formatDate(exp.start_date, "auto", $i18n.locale) }} <span v-if="exp.end_date"> - {{ formatDate(exp.end_date, "auto", $i18n.locale) }}</span><span v-else-if="exp.is_current"> - {{ $t('experience.present') }}</span>
        </time>
        <div class=" text-neutral-300 text-base mb-2">
          {{ getTranslation(exp, $i18n.locale).responsibilities }}
        </div>
        <p class="italic text-neutral-400  whitespace-pre-line">
          {{ getTranslation(exp, $i18n.locale).description }}
        </p>
      </li>
    </ol>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";

import { formatDate } from '@/common/helpers/dateFormat'

import { useExperienceStore } from "@/stores/experience";
const experienceStore = useExperienceStore();
const experiences = ref([]);

const sectionId = "experience"

// --- СПИСОК ОПЫТА ---

// Переменные пагинированного списка
const page = ref(1);
const limit = 5;
const total = ref(0);
const hasNextPage = ref(true);

// Переменная процесса загрузки
const loading = ref(false);

const fetchProjects = async (reset = false) => {
  if (loading.value) return;
  loading.value = true;

  if (reset) {
    experiences.value = [];
    page.value = 1;
    hasNextPage.value = true;
  }

  const params = {
    offset: page.value,
    limit,
  };

  const data = await experienceStore.loadExperiences({ params });

  if (data) {
    if (reset) {
      experiences.value = data.items;
    } else {
      experiences.value.push(...data.items);
    }
    total.value = data.total;
    hasNextPage.value = data.has_next;
    page.value += 1;
  } else {
    hasNextPage.value = false;
  }

  loading.value = false;
};

function getTranslation(proj, currentLang) {
  return proj.translations?.find(t => t.lang === currentLang) ||
    proj.translations?.[0] ||
    { title: proj.title, description: "" };
}

onMounted(() => fetchProjects(true));
</script>