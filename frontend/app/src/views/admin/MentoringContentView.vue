<template>
  <div>
    <div class="d-flex align-center justify-space-between flex-wrap ga-3 mb-4">
      <div>
        <h1 class="text-h5">Контент наставничества</h1>
        <p class="text-body-2 text-medium-emphasis mt-1">Заголовок секции, вводный текст и показатели</p>
      </div>
      <v-btn color="primary" :loading="saving" @click="save">
        <v-icon start>mdi-content-save</v-icon>Сохранить
      </v-btn>
    </div>

    <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>
    <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />

    <v-form v-if="!loading" ref="formRef" @submit.prevent="save">
      <v-switch v-model="form.is_published" label="Секция опубликована" color="primary" class="mb-2" />

      <v-tabs v-model="currentLang" bg-color="grey-lighten-4" grow class="mb-4">
        <v-tab v-for="translation in form.translations" :key="translation.lang" :value="translation.lang">
          {{ LANGS[translation.lang] || translation.lang.toUpperCase() }}
        </v-tab>
      </v-tabs>

      <v-card variant="outlined" class="mb-6">
        <v-card-text>
          <div v-for="translation in form.translations" :key="translation.lang" v-show="currentLang === translation.lang">
            <v-text-field v-model="translation.kicker" label="Надзаголовок" :rules="requiredRules" />
            <v-row>
              <v-col cols="12" md="6"><v-text-field v-model="translation.title_start" label="Заголовок" :rules="requiredRules" /></v-col>
              <v-col cols="12" md="6"><v-text-field v-model="translation.title_accent" label="Акцент заголовка" :rules="requiredRules" /></v-col>
            </v-row>
            <v-textarea v-model="translation.lead" label="Вводный текст" rows="4" auto-grow :rules="requiredRules" />
          </div>
        </v-card-text>
      </v-card>

      <div class="d-flex align-center justify-space-between flex-wrap ga-3 mb-3">
        <h2 class="text-h6">Показатели</h2>
        <v-btn variant="tonal" @click="addMetric"><v-icon start>mdi-plus</v-icon>Добавить показатель</v-btn>
      </div>

      <v-card v-for="(metric, index) in form.metrics" :key="metric.id || index" variant="outlined" class="mb-3">
        <v-card-text>
          <div class="d-flex align-start ga-2">
            <v-row class="grow">
              <v-col cols="12" sm="4"><v-text-field v-model="metric.key" label="Ключ" hint="Например, projects" persistent-hint :rules="requiredRules" /></v-col>
              <v-col cols="12" sm="3"><v-text-field v-model="metric.value" label="Значение" :rules="requiredRules" /></v-col>
              <v-col cols="12" sm="5">
                <v-text-field v-model="metricTranslation(metric).label" :label="`Подпись (${LANGS[currentLang]})`" :rules="requiredRules" />
              </v-col>
            </v-row>
            <v-btn icon="mdi-delete" variant="text" color="error" :aria-label="`Удалить показатель ${index + 1}`"
              @click="removeMetric(index)" />
          </div>
        </v-card-text>
      </v-card>
      <v-alert v-if="!form.metrics.length" type="info" variant="tonal">Показатели не добавлены.</v-alert>
    </v-form>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { LANGS } from '@/common/constants/langs'
import { useMentoringStore } from '@/stores/mentoring'

const store = useMentoringStore()
const currentLang = ref('ru')
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const formRef = ref(null)
const requiredRules = [(value) => !!String(value ?? '').trim() || 'Поле обязательно']

function blankMetricTranslation(lang) {
  return { lang, label: '' }
}

function blankPage() {
  return {
    is_published: true,
    translations: [
      { lang: 'ru', kicker: '', title_start: '', title_accent: '', lead: '' },
      { lang: 'en', kicker: '', title_start: '', title_accent: '', lead: '' },
    ],
    metrics: [],
  }
}

const form = ref(blankPage())

function normalizeContent(content) {
  const normalized = blankPage()
  Object.assign(normalized, content)
  normalized.translations = normalized.translations.map((translation) => ({
    kicker: '', title_start: '', title_accent: '', lead: '', ...translation,
  }))
  normalized.metrics = normalized.metrics.map((metric) => ({
    ...metric,
    translations: metric.translations?.length
      ? metric.translations.map((translation) => ({ ...translation }))
      : [blankMetricTranslation('ru'), blankMetricTranslation('en')],
  }))
  currentLang.value = normalized.translations.some((item) => item.lang === 'ru') ? 'ru' : normalized.translations[0]?.lang
  return normalized
}

function metricTranslation(metric) {
  return metric.translations.find((translation) => translation.lang === currentLang.value)
    || metric.translations[0]
}

function addMetric() {
  const index = form.value.metrics.length + 1
  form.value.metrics.push({
    key: `metric_${index}`,
    value: '',
    order: index - 1,
    translations: [blankMetricTranslation('ru'), blankMetricTranslation('en')],
  })
}

function removeMetric(index) {
  form.value.metrics.splice(index, 1)
  form.value.metrics.forEach((metric, order) => { metric.order = order })
}

async function load() {
  loading.value = true
  error.value = ''
  const content = await store.loadAdminMentoringContent()
  if (content) form.value = normalizeContent(content)
  else error.value = 'Не удалось загрузить контент наставничества.'
  loading.value = false
}

async function save() {
  const validation = await formRef.value?.validate()
  if (!validation?.valid) return

  saving.value = true
  error.value = ''
  const payload = {
    is_published: form.value.is_published,
    translations: form.value.translations.map(({ lang, kicker, title_start, title_accent, lead }) => ({
      lang, kicker, title_start, title_accent, lead,
    })),
    metrics: form.value.metrics.map((metric, order) => ({
      key: metric.key.trim(),
      value: metric.value.trim(),
      order,
      translations: metric.translations.map(({ lang, label }) => ({ lang, label })),
    })),
  }
  const result = await store.updateMentoringContent(payload)
  saving.value = false
  if (!result) {
    error.value = 'Не удалось сохранить контент наставничества.'
    return
  }
  form.value = normalizeContent(result)
}

onMounted(load)
</script>
