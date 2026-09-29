<template>
  <div>
    <div class="d-flex flex-wrap align-center justify-space-between ga-2 mb-4">
      <h1 class="text-h5">Обращения</h1>
      <v-btn variant="text" prepend-icon="mdi-refresh" :loading="loading" @click="reload">Обновить</v-btn>
    </div>

    <!-- Счётчики -->
    <div v-if="stats" class="d-flex flex-wrap ga-2 mb-4">
      <v-chip color="primary" variant="tonal" prepend-icon="mdi-bell-outline">Новые: {{ stats.new }}</v-chip>
      <v-chip variant="tonal" prepend-icon="mdi-briefcase-outline">Заказы: {{ stats.orders }}</v-chip>
      <v-chip variant="tonal" prepend-icon="mdi-school-outline">Обучение: {{ stats.trainings }}</v-chip>
      <v-chip variant="tonal" prepend-icon="mdi-help-circle-outline">Вопросы: {{ stats.questions }}</v-chip>
      <v-chip v-if="stats.email_failed" color="red" variant="tonal" prepend-icon="mdi-email-alert-outline">
        Не доставлено на почту: {{ stats.email_failed }}
      </v-chip>
    </div>

    <!-- Фильтры -->
    <v-row dense class="mb-2">
      <v-col cols="12" md="4">
        <v-btn-toggle v-model="filters.kind" mandatory density="comfortable" variant="outlined" divided class="w-100">
          <v-btn value="" class="flex-grow-1">Все</v-btn>
          <v-btn value="order" class="flex-grow-1">Заказы</v-btn>
          <v-btn value="training" class="flex-grow-1">Обучение</v-btn>
          <v-btn value="question" class="flex-grow-1">Вопросы</v-btn>
        </v-btn-toggle>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-select v-model="filters.status" :items="statusFilterItems" label="Статус" density="comfortable"
          hide-details clearable />
      </v-col>
      <v-col cols="12" sm="6" md="5">
        <v-text-field v-model="filters.search" label="Поиск: имя, email, текст" density="comfortable" hide-details
          clearable prepend-inner-icon="mdi-magnify" />
      </v-col>
    </v-row>

    <!-- Список -->
    <v-card v-for="item in items" :key="item.id" class="mb-3" :class="{ 'feedback--new': item.status === 'new' }"
      variant="outlined">
      <v-card-item>
        <template #prepend>
          <v-avatar :color="kindMeta(item).color" variant="tonal">
            <v-icon>{{ kindMeta(item).icon }}</v-icon>
          </v-avatar>
        </template>
        <v-card-title class="d-flex flex-wrap align-center ga-2">
          {{ item.name }}
          <v-chip size="x-small" :color="kindMeta(item).color" label>
            {{ kindMeta(item).title }}
          </v-chip>
          <v-chip v-if="item.lang" size="x-small" label variant="outlined">{{ item.lang.toUpperCase() }}</v-chip>
        </v-card-title>
        <v-card-subtitle class="d-flex flex-wrap ga-3">
          <a :href="`mailto:${item.email}`">{{ item.email }}</a>
          <span v-if="item.contact"><v-icon size="small">mdi-account-box-outline</v-icon> {{ item.contact }}</span>
          <span>{{ formatDateTime(item.created_at) }}</span>
        </v-card-subtitle>
        <template #append>
          <v-tooltip :text="emailTooltip(item)" location="top" max-width="420">
            <template #activator="{ props }">
              <v-chip v-bind="props" size="small" :color="emailStatus(item).color" variant="tonal"
                :prepend-icon="emailStatus(item).icon">
                {{ emailStatus(item).title }}
              </v-chip>
            </template>
          </v-tooltip>
        </template>
      </v-card-item>

      <v-card-text>
        <div v-if="item.kind !== 'question'" class="d-flex flex-wrap ga-2 mb-3">
          <v-chip v-if="item.service" size="small" prepend-icon="mdi-shape-outline">{{ serviceLabel(item) }}</v-chip>
          <v-chip v-if="item.budget" size="small" prepend-icon="mdi-cash">{{ BUDGET_LABELS[item.budget] || item.budget }}</v-chip>
          <v-chip v-if="item.deadline" size="small" prepend-icon="mdi-calendar-clock">{{ item.deadline }}</v-chip>
        </div>
        <div class="feedback__message">{{ item.message }}</div>

        <v-row dense class="mt-3">
          <v-col cols="12" sm="4">
            <v-select :model-value="item.status" :items="STATUS_OPTIONS" item-title="title" item-value="value"
              label="Статус" density="compact" hide-details @update:model-value="(v) => save(item, { status: v })">
              <template #selection="{ item: opt }">
                <v-chip size="small" :color="opt.raw.color" label>{{ opt.raw.title }}</v-chip>
              </template>
            </v-select>
          </v-col>
          <v-col cols="12" sm="8">
            <v-text-field v-model="notes[item.id]" label="Заметка (видна только вам)" density="compact" hide-details
              :append-inner-icon="notes[item.id] !== (item.admin_note || '') ? 'mdi-content-save' : undefined"
              @click:append-inner="save(item, { admin_note: notes[item.id] })"
              @keyup.enter="save(item, { admin_note: notes[item.id] })" />
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions class="flex-wrap">
        <v-btn color="primary" variant="tonal" prepend-icon="mdi-reply" :href="replyLink(item)">Ответить</v-btn>
        <v-btn v-if="item.email_status !== 'sent'" variant="text" prepend-icon="mdi-email-sync-outline"
          :loading="busy[item.id] === 'resend'" @click="resend(item)">
          Отправить письмо ещё раз
        </v-btn>
        <v-spacer />
        <v-btn color="red" variant="text" icon="mdi-delete-outline" :loading="busy[item.id] === 'delete'"
          @click="remove(item)" />
      </v-card-actions>
    </v-card>

    <v-alert v-if="!loading && !items.length" type="info" variant="tonal" class="mt-4">
      Обращений пока нет
    </v-alert>

    <div class="text-center my-4">
      <v-btn v-if="hasNextPage && !loading" variant="outlined" @click="fetchPage()">Показать ещё</v-btn>
      <v-progress-circular v-if="loading" indeterminate color="primary" />
    </div>

    <v-snackbar v-model="snackbar.visible" :color="snackbar.color" timeout="2500">{{ snackbar.text }}</v-snackbar>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue'

import { useFeedbackStore } from '@/stores/feedback'
import {
  SERVICE_LABELS,
  TRAINING_LABELS,
  KIND_META,
  BUDGET_LABELS,
  STATUS_OPTIONS,
  EMAIL_STATUS,
} from '@/common/constants/feedback'

const feedbackStore = useFeedbackStore()

const items = ref([])
const stats = ref(null)
const notes = reactive({})
const busy = reactive({})
const loading = ref(false)
const page = ref(0)
const limit = 20
const hasNextPage = ref(true)
const filters = reactive({ kind: '', status: null, search: '' })
const snackbar = reactive({ visible: false, text: '', color: 'success' })

const statusFilterItems = STATUS_OPTIONS.map(({ value, title }) => ({ value, title }))

function notify(text, color = 'success') {
  Object.assign(snackbar, { visible: true, text, color })
}

function formatDateTime(value) {
  return new Date(value).toLocaleString('ru', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function emailStatus(item) {
  return EMAIL_STATUS[item.email_status] || EMAIL_STATUS.pending
}

function emailTooltip(item) {
  const parts = [`Попыток: ${item.email_attempts}`]
  if (item.email_provider) parts.push(`через ${item.email_provider}`)
  if (item.emailed_at) parts.push(formatDateTime(item.emailed_at))
  if (item.email_error) parts.push(item.email_error)
  return parts.join(' · ')
}

function kindMeta(item) {
  return KIND_META[item.kind] || KIND_META.question
}

function serviceLabel(item) {
  const labels = item.kind === 'training' ? TRAINING_LABELS : SERVICE_LABELS
  return labels[item.service] || item.service
}

function replyLink(item) {
  const subject = kindMeta(item).subject
  const quote = item.message.split('\n').map((l) => `> ${l}`).join('\n')
  return `mailto:${item.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(`\n\n${quote}`)}`
}

function upsert(updated) {
  const index = items.value.findIndex((i) => i.id === updated.id)
  if (index !== -1) items.value[index] = updated
  notes[updated.id] = updated.admin_note || ''
}

async function fetchPage(reset = false) {
  if (loading.value) return
  loading.value = true

  if (reset) {
    items.value = []
    page.value = 0
    hasNextPage.value = true
  }

  const params = { offset: page.value + 1, limit }
  if (filters.kind) params.kind = filters.kind
  if (filters.status) params.status = filters.status
  if (filters.search) params.search = filters.search

  const data = await feedbackStore.loadFeedback({ params })
  if (data) {
    items.value.push(...data.items)
    data.items.forEach((i) => { notes[i.id] = i.admin_note || '' })
    hasNextPage.value = data.has_next
    page.value += 1
  } else {
    hasNextPage.value = false
  }
  loading.value = false
}

async function loadStats() {
  stats.value = await feedbackStore.loadFeedbackStats()
}

async function reload() {
  await Promise.all([fetchPage(true), loadStats()])
}

async function save(item, data) {
  const updated = await feedbackStore.updateFeedback(item.id, data)
  if (!updated) return notify('Не удалось сохранить', 'error')
  upsert(updated)
  loadStats()
  notify('Сохранено')
}

async function resend(item) {
  busy[item.id] = 'resend'
  const updated = await feedbackStore.resendFeedback(item.id)
  busy[item.id] = null
  if (!updated) return notify('Ошибка запроса', 'error')
  upsert(updated)
  loadStats()
  notify(updated.email_status === 'sent' ? 'Письмо отправлено' : 'Не удалось отправить письмо', updated.email_status === 'sent' ? 'success' : 'error')
}

async function remove(item) {
  if (!confirm(`Удалить обращение от «${item.name}»?`)) return
  busy[item.id] = 'delete'
  const ok = await feedbackStore.deleteFeedback(item.id)
  busy[item.id] = null
  if (!ok) return notify('Не удалось удалить', 'error')
  items.value = items.value.filter((i) => i.id !== item.id)
  loadStats()
}

let searchTimer = null
watch(() => [filters.kind, filters.status], () => fetchPage(true))
watch(() => filters.search, () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => fetchPage(true), 400)
})

onMounted(reload)
</script>

<style scoped>
.feedback--new {
  border-left: 4px solid rgb(var(--v-theme-primary));
}

.feedback__message {
  white-space: pre-line;
  font-size: 0.95rem;
  line-height: 1.6;
  color: rgba(var(--v-theme-on-surface), 0.9);
}
</style>
