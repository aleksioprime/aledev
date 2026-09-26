<template>
  <section :id="sectionId" class="section">
    <div class="shell">
      <header class="section-head mentoring-head">
        <div>
          <span v-reveal class="section-kicker">03 — {{ t('mentoring.kicker') }}</span>
          <h2 v-reveal="{ delay: 80 }" class="section-title">
            {{ t('mentoring.titleStart') }} <span class="text-gradient">{{ t('mentoring.titleAccent') }}</span>
          </h2>
        </div>
        <p v-reveal="{ delay: 160 }" class="section-lead">{{ t('mentoring.lead') }}</p>
      </header>

      <dl class="numbers">
        <div v-for="(n, i) in numbers" :key="n.key" v-reveal="{ variant: 'scale', delay: i * 80 }" class="number">
          <dt class="number__label">{{ t(`mentoring.numbers.${n.key}`) }}</dt>
          <dd class="number__value font-display">{{ n.value }}</dd>
        </div>
      </dl>

      <div class="grid">
        <!-- Гранты, конкурсы и исследования -->
        <div class="col">
          <h3 v-reveal class="col__title">
            <Icon :path="mdiTrophyOutline" />
            {{ t('mentoring.awardsTitle') }}
          </h3>
          <ul class="awards">
            <li v-for="(item, i) in awards" :key="item.key" v-reveal="{ delay: i * 70 }" class="award glass">
              <span class="award__year font-mono">{{ item.year }}</span>
              <div>
                <p class="award__title">{{ t(`mentoring.awards.${item.key}.title`) }}</p>
                <p class="award__text">{{ t(`mentoring.awards.${item.key}.text`) }}</p>
              </div>
            </li>
          </ul>
        </div>

        <!-- Результаты ученических команд -->
        <div class="col">
          <h3 v-reveal class="col__title">
            <Icon :path="mdiAccountGroupOutline" />
            {{ t('mentoring.teamsTitle') }}
          </h3>
          <ul class="results">
            <li v-for="(item, i) in results" :key="item.key" v-reveal="{ variant: 'right', delay: i * 60 }"
              class="result">
              <span class="result__place">{{ t(`mentoring.results.${item.key}.place`) }}</span>
              <span class="result__body">
                <span class="result__title">{{ t(`mentoring.results.${item.key}.title`) }}</span>
                <span class="result__text">{{ t(`mentoring.results.${item.key}.text`) }}</span>
              </span>
              <span class="result__year font-mono">{{ item.year }}</span>
            </li>
          </ul>

          <p v-reveal class="expert">
            <Icon :path="mdiScaleBalance" />
            {{ t('mentoring.expert') }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import Icon from '@/components/ui/Icon.vue'
import { mdiAccountGroupOutline, mdiScaleBalance, mdiTrophyOutline } from '@mdi/js'
import { useI18n } from 'vue-i18n'

// Факты — из педагогического портфолио (Международная гимназия «Сколково», 2016–2022)
const sectionId = 'mentoring'
const { t } = useI18n()

const numbers = [
  { key: 'projects', value: '30+' },
  { key: 'prizes', value: '15+' },
  { key: 'programs', value: '6' },
]

const awards = [
  { key: 'umnik', year: '2019' },
  { key: 'intel', year: '2021' },
  { key: 'pedcom', year: '2021' },
  { key: 'trainer', year: '2020' },
  { key: 'hackathon', year: '2018' },
]

const results = [
  { key: 'intelStudents', year: '2022' },
  { key: 'firstRussia', year: '2020' },
  { key: 'worldskills', year: '2019' },
  { key: 'prizma', year: '2018' },
  { key: 'eurobot', year: '2017' },
  { key: 'shustrik', year: '2017' },
]
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

.grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: clamp(2rem, 5vw, 4rem);
  align-items: start;
}

.col__title {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 1.25rem;
  font-size: 1.15rem;
  font-weight: 700;
}

.col__title .icon {
  color: var(--accent);
}

.awards {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.award {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1rem;
  padding: 1.1rem 1.25rem;
  transition: border-color 0.3s ease;
}

.award:hover {
  border-color: rgb(34 211 238 / 0.35);
}

.award__year {
  padding-top: 0.15rem;
  font-size: 0.8rem;
  color: var(--accent);
}

.award__title {
  font-weight: 700;
  line-height: 1.4;
}

.award__text {
  margin-top: 0.35rem;
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--muted);
}

.results {
  margin: 0;
  padding: 0;
  list-style: none;
  border-top: 1px solid var(--line);
}

.result {
  display: grid;
  grid-template-columns: 5.5rem 1fr auto;
  align-items: baseline;
  gap: 1rem;
  padding: 1rem 0.25rem;
  border-bottom: 1px solid var(--line);
}

.result__place {
  font-weight: 700;
  color: var(--accent-3);
}

.result__body {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.result__title {
  font-weight: 600;
  line-height: 1.4;
}

.result__text {
  font-size: 0.88rem;
  line-height: 1.55;
  color: var(--muted);
}

.result__year {
  font-size: 0.78rem;
  color: var(--muted);
}

.expert {
  display: flex;
  gap: 0.6rem;
  margin-top: 1.5rem;
  font-size: 0.92rem;
  line-height: 1.6;
  color: var(--muted);
}

.expert .icon {
  margin-top: 0.2rem;
  color: var(--accent-2);
}

@media (max-width: 900px) {
  .grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 540px) {
  .number {
    padding: 0.8rem 0.75rem;
  }

  .number__label {
    font-size: 0.75rem;
  }

  .result {
    grid-template-columns: 1fr auto;
  }

  .result__place {
    grid-column: 1 / -1;
  }
}
</style>
