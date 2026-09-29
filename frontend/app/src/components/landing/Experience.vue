<template>
  <section :id="sectionId" class="section">
    <div class="shell exp">
      <header class="section-head exp__head">
        <span v-reveal class="section-kicker">04 — {{ $t('experience.kicker') }}</span>
        <h2 v-reveal="{ delay: 80 }" class="section-title">{{ $t('experience.sectionTitle') }}</h2>
        <p v-reveal="{ delay: 160 }" class="section-lead">{{ $t('experience.lead') }}</p>
      </header>

      <ol ref="listRef" class="timeline" :style="{ '--progress': progress }">
        <li v-for="(exp, i) in experiences" :key="exp.id" v-reveal="{ variant: 'right', delay: 60 }"
          class="timeline__item" :class="{ 'is-current': exp.is_current }">
          <span class="timeline__dot" aria-hidden="true"></span>

          <div class="timeline__meta font-mono">
            <time>{{ formatDate(exp.start_date, "auto", $i18n.locale) }}</time>
            <span class="timeline__dash">—</span>
            <time v-if="exp.end_date">{{ formatDate(exp.end_date, "auto", $i18n.locale) }}</time>
            <span v-else-if="exp.is_current" class="timeline__now">{{ $t('experience.present') }}</span>
          </div>

          <div class="timeline__card glass">
            <span class="timeline__num font-mono">{{ String(experiences.length - i).padStart(2, '0') }}</span>
            <h3 class="timeline__position">{{ getTranslation(exp, $i18n.locale).position }}</h3>
            <p class="timeline__company">{{ getTranslation(exp, $i18n.locale).company }}</p>
            <p v-if="getTranslation(exp, $i18n.locale).responsibilities" class="timeline__resp">
              {{ getTranslation(exp, $i18n.locale).responsibilities }}
            </p>
            <p v-if="getTranslation(exp, $i18n.locale).description" class="timeline__desc">
              {{ getTranslation(exp, $i18n.locale).description }}
            </p>
          </div>
        </li>
      </ol>

      <div v-if="hasNextPage && experiences.length" class="exp__more">
        <button v-magnetic type="button" class="btn btn-ghost" :disabled="loading" @click="fetchExperiences()">
          {{ $t('experience.showMore') }}
          <Icon :path="mdiChevronDown" />
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import Icon from '@/components/ui/Icon.vue'
import { mdiChevronDown } from '@mdi/js'
import { onBeforeUnmount, onMounted, ref } from "vue";

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

const fetchExperiences = async (reset = false) => {
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

// --- Линия таймлайна «прорисовывается» по мере прокрутки ---
const listRef = ref(null);
const progress = ref(0);
let rafId = 0;

function onScroll() {
  cancelAnimationFrame(rafId);
  rafId = requestAnimationFrame(() => {
    const el = listRef.value;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const start = window.innerHeight * 0.75;
    const value = (start - rect.top) / rect.height;
    progress.value = Math.max(0, Math.min(1, value));
  });
}

onMounted(() => {
  fetchExperiences(true);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
});

onBeforeUnmount(() => {
  cancelAnimationFrame(rafId);
  window.removeEventListener('scroll', onScroll);
});
</script>

<style scoped>
.exp {
  display: grid;
  grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
  gap: clamp(2rem, 6vw, 5rem);
  align-items: start;
}

.exp__head {
  position: sticky;
  top: 7rem;
}

.timeline {
  position: relative;
  margin: 0;
  padding: 0 0 0 2.25rem;
  list-style: none;
}

/* базовая линия */
.timeline::before,
.timeline::after {
  content: "";
  position: absolute;
  top: 0.4rem;
  bottom: 0;
  left: 0.45rem;
  width: 2px;
  border-radius: 2px;
}

.timeline::before {
  background: var(--line);
}

/* заполненная часть */
.timeline::after {
  background: linear-gradient(var(--accent), var(--accent-2));
  box-shadow: 0 0 12px rgb(var(--accent-rgb) / 0.6);
  transform: scaleY(var(--progress, 0));
  transform-origin: top;
}

.timeline__item {
  position: relative;
  padding-bottom: 2.5rem;
}

.timeline__item:last-child {
  padding-bottom: 0;
}

.timeline__dot {
  position: absolute;
  top: 0.3rem;
  left: -2.25rem;
  z-index: 1;
  width: 1.1rem;
  height: 1.1rem;
  border: 2px solid var(--accent);
  border-radius: 50%;
  background: var(--bg);
}

.is-current .timeline__dot {
  background: var(--accent);
  box-shadow: 0 0 0 6px rgb(var(--accent-rgb) / 0.15);
}

.timeline__meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.8rem;
  font-size: 0.8rem;
  color: var(--muted);
  text-transform: capitalize;
}

.timeline__dash {
  opacity: 0.5;
}

.timeline__now {
  padding: 0.1rem 0.55rem;
  border-radius: 999px;
  background: rgb(var(--accent-3-rgb) / 0.12);
  color: var(--accent-3);
}

.timeline__card {
  position: relative;
  padding: 1.5rem 1.6rem;
  transition: border-color 0.4s ease, transform 0.5s var(--ease-out);
}

.timeline__card:hover {
  border-color: rgb(var(--accent-rgb) / 0.3);
  transform: translateX(6px);
}

.timeline__num {
  position: absolute;
  top: 1.2rem;
  right: 1.4rem;
  font-size: 0.75rem;
  color: rgb(255 255 255 / 0.2);
}

.timeline__position {
  padding-right: 2rem;
  font-size: 1.2rem;
  font-weight: 700;
  line-height: 1.3;
}

.timeline__company {
  margin-top: 0.3rem;
  font-weight: 600;
  color: var(--accent);
}

.timeline__resp {
  margin-top: 0.9rem;
  line-height: 1.7;
  color: var(--text);
}

.timeline__desc {
  margin-top: 0.7rem;
  white-space: pre-line;
  font-size: 0.93rem;
  line-height: 1.7;
  color: var(--muted);
}

.exp__more {
  grid-column: 2;
  padding-left: 2.25rem;
}

@media (max-width: 900px) {
  .exp {
    grid-template-columns: 1fr;
  }

  .exp__head {
    position: static;
  }

  .exp__more {
    grid-column: 1;
  }
}
</style>
