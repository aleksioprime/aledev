<template>
  <section :id="sectionId" class="section">
    <div class="shell">
      <header class="section-head mentoring-head">
        <div>
          <span v-if="pageTranslation" v-reveal class="section-kicker">03 — {{ pageTranslation.kicker }}</span>
          <h2 v-if="pageTranslation" v-reveal="{ delay: 80 }" class="section-title">
            {{ pageTranslation.title_start }} <span class="text-gradient">{{ pageTranslation.title_accent }}</span>
          </h2>
          <p v-else class="section-lead">{{ contentLoading ? t('mentoring.contentLoading') : t('mentoring.contentUnavailable') }}</p>
        </div>
        <p v-if="pageTranslation" v-reveal="{ delay: 160 }" class="section-lead">{{ pageTranslation.lead }}</p>
      </header>

      <dl v-if="metrics.length" class="numbers">
        <div v-for="(n, i) in metrics" :key="n.key" v-reveal="{ variant: 'scale', delay: i * 80 }" class="number">
          <dt class="number__label">{{ n.label }}</dt>
          <dd class="number__value font-display">{{ n.value }}</dd>
        </div>
      </dl>

      <div class="achievement-toolbar" aria-label="Фильтры достижений">
        <div class="filter-group" role="group" :aria-label="t('mentoring.filterCategory')">
          <button type="button" class="filter-button" :class="{ 'filter-button--active': selectedCategory === 'all' }"
            @click="selectedCategory = 'all'">{{ t('mentoring.allCategories') }}</button>
          <button v-for="category in categories" :key="category" type="button" class="filter-button"
            :class="{ 'filter-button--active': selectedCategory === category }"
            @click="selectedCategory = category">{{ categoryLabel(category) }}</button>
        </div>
        <div class="filter-group filter-group--scope" role="group" :aria-label="t('mentoring.filterScope')">
          <button v-for="scope in scopes" :key="scope" type="button" class="filter-button"
            :class="{ 'filter-button--active': selectedScope === scope }"
            @click="selectedScope = scope">{{ t(`mentoring.scope.${scope}`) }}</button>
        </div>
      </div>

      <p v-if="loading" class="achievements-state">{{ t('mentoring.loading') }}</p>
      <p v-else-if="!filteredAchievements.length" class="achievements-state">{{ t('mentoring.empty') }}</p>
      <ol v-else class="achievement-list">
        <li v-for="(item, i) in filteredAchievements" :key="item.id" v-reveal="{ delay: Math.min(i * 45, 270) }">
          <article class="achievement">
            <div class="achievement__meta">
              <span v-if="item.year" class="achievement__year font-mono">{{ item.year }}</span>
              <span class="achievement__scope">{{ t(`mentoring.scope.${item.scope}`) }}</span>
            </div>
            <div class="achievement__content">
              <div class="achievement__heading">
                <h3 class="achievement__title">{{ translationFor(item).title }}</h3>
                <span v-if="translationFor(item).result" class="achievement__result">{{ translationFor(item).result }}</span>
              </div>
              <p v-if="translationFor(item).organization" class="achievement__organization">
                {{ translationFor(item).organization }}
              </p>
              <p v-if="translationFor(item).short_description || translationFor(item).description" class="achievement__description">
                {{ translationFor(item).short_description || translationFor(item).description }}
              </p>
              <a v-if="item.source_url" class="achievement__source" :href="item.source_url" target="_blank"
                rel="noopener noreferrer">{{ t('mentoring.source') }}</a>
            </div>
            <span class="achievement__category font-mono">{{ categoryLabel(item.category) }}</span>
          </article>
        </li>
      </ol>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAchievementStore } from '@/stores/achievement'
import { useMentoringStore } from '@/stores/mentoring'

const sectionId = 'mentoring'
const { t, locale } = useI18n()
const achievementStore = useAchievementStore()
const mentoringStore = useMentoringStore()
const achievements = ref([])
const pageContent = ref(null)
const loading = ref(true)
const contentLoading = ref(true)
const selectedCategory = ref('all')
const selectedScope = ref('all')

const scopes = ['all', 'personal', 'students']
const pageTranslation = computed(() => pageContent.value?.translations?.find((translation) => translation.lang === locale.value)
  || pageContent.value?.translations?.find((translation) => translation.lang === 'ru')
  || pageContent.value?.translations?.[0]
  || null)
const metrics = computed(() => (pageContent.value?.metrics || []).map((metric) => ({
  ...metric,
  label: metric.translations?.find((translation) => translation.lang === locale.value)?.label
    || metric.translations?.find((translation) => translation.lang === 'ru')?.label
    || metric.translations?.[0]?.label
    || '',
})))
const categories = computed(() => [...new Set(achievements.value.map((item) => item.category))])
const filteredAchievements = computed(() => achievements.value.filter((item) =>
  (selectedCategory.value === 'all' || item.category === selectedCategory.value)
  && (selectedScope.value === 'all' || item.scope === selectedScope.value)
))

function translationFor(item) {
  return item.translations?.find((translation) => translation.lang === locale.value)
    || item.translations?.find((translation) => translation.lang === 'ru')
    || item.translations?.[0]
    || {}
}

function categoryLabel(category) {
  return t(`mentoring.categories.${category}`)
}

onMounted(async () => {
  const [content, achievementsData] = await Promise.all([
    mentoringStore.loadMentoringContent(),
    achievementStore.loadAchievements({ params: { offset: 0, limit: 100 } }),
  ])
  pageContent.value = content
  achievements.value = achievementsData?.items || []
  contentLoading.value = false
  loading.value = false
})
</script>

<style scoped>
.mentoring-head {
  flex-direction: row;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1.5rem 3rem;
}

.mentoring-head > div {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.numbers {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-bottom: clamp(2.5rem, 5vw, 3.5rem);
}

.number {
  display: flex;
  flex-direction: column-reverse;
  gap: 0.35rem;
  padding: 1rem 1.25rem;
  border-left: 1px solid var(--line-strong);
}

.number__value {
  margin: 0;
  font-size: clamp(2rem, 4.5vw, 3rem);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.03em;
}

.number__label {
  font-size: 0.85rem;
  color: var(--muted);
}

.achievement-toolbar {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 0.75rem 1.5rem;
  margin-bottom: 1.5rem;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.filter-button {
  min-height: 2.35rem;
  padding: 0.4rem 0.75rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: transparent;
  color: var(--muted);
  font-size: 0.82rem;
  cursor: pointer;
  transition: color 0.2s ease, border-color 0.2s ease, background-color 0.2s ease;
}

.filter-button:hover,
.filter-button--active {
  border-color: var(--accent);
  background: rgb(var(--accent-rgb) / 0.08);
  color: var(--text);
}

.filter-button:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.achievement-list {
  margin: 0;
  padding: 0;
  border-top: 1px solid var(--line);
  list-style: none;
}

.achievement-list > li {
  border-bottom: 1px solid var(--line);
}

.achievement {
  display: grid;
  /* фиксированные крайние колонки, чтобы заголовки строк были на одной линии */
  grid-template-columns: 9rem minmax(0, 1fr) 9.5rem;
  align-items: start;
  gap: 1.25rem;
  padding: 1.25rem 0.25rem;
}

.achievement__meta {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  padding-top: 0.1rem;
}

.achievement__year,
.achievement__category {
  font-size: 0.76rem;
  color: var(--accent);
}

.achievement__category {
  text-align: right;
}

.achievement__scope {
  font-size: 0.8rem;
  color: var(--muted);
}

.achievement__heading {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.5rem 0.8rem;
}

.achievement__title {
  font-size: 1.05rem;
  font-weight: 650;
  line-height: 1.45;
}

.achievement__result {
  color: var(--accent-3);
  font-size: 0.9rem;
  font-weight: 700;
}

.achievement__organization {
  margin-top: 0.25rem;
  color: var(--muted);
  font-size: 0.85rem;
}

.achievement__description {
  max-width: 54rem;
  margin-top: 0.5rem;
  color: var(--muted);
  font-size: 0.9rem;
  line-height: 1.65;
}

.achievement__source {
  display: inline-block;
  margin-top: 0.55rem;
  color: var(--accent);
  font-size: 0.82rem;
}

.achievements-state {
  padding-block: 2rem;
  color: var(--muted);
}

@media (max-width: 540px) {
  .number {
    padding: 0.8rem 0.75rem;
  }

  .number__label {
    font-size: 0.75rem;
  }

  .achievement {
    grid-template-columns: 1fr auto;
    gap: 0.55rem 0.8rem;
  }

  .achievement__meta {
    grid-column: 1 / -1;
    flex-direction: row;
    align-items: baseline;
    gap: 0.75rem;
  }

  .achievement__content {
    min-width: 0;
  }

  .achievement__category {
    grid-column: 2;
    grid-row: 2;
    justify-self: end;
    max-width: 7.5rem;
    text-align: right;
  }

  .achievement__heading {
    display: block;
  }

  .achievement__result {
    display: inline-block;
    margin-top: 0.25rem;
  }
}
</style>
