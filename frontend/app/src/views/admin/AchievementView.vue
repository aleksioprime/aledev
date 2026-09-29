<template>
  <div>
    <div class="d-flex align-center justify-space-between flex-wrap ga-3 mb-4">
      <div>
        <h1 class="text-h5">Достижения</h1>
        <p class="text-body-2 text-medium-emphasis mt-1">Награды, проекты учеников, сертификации и экспертная деятельность</p>
      </div>
      <v-btn color="primary" @click="openEditor()"><v-icon start>mdi-plus</v-icon>Добавить достижение</v-btn>
    </div>

    <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>
    <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-3" />
    <v-list v-if="achievements.length" class="pa-0">
      <v-list-item v-for="item in achievements" :key="item.id" class="border-b">
        <v-list-item-title class="font-weight-medium">
          {{ translationFor(item).title || 'Без названия' }}
          <v-chip v-if="translationFor(item).result" size="small" color="primary" class="ms-2">{{ translationFor(item).result }}</v-chip>
          <v-chip v-if="!item.is_published" size="small" color="warning" class="ms-1">Черновик</v-chip>
        </v-list-item-title>
        <v-list-item-subtitle>
          {{ item.year || 'Без года' }} · {{ categoryLabel(item.category) }} · {{ scopeLabel(item.scope) }}
          <span v-if="translationFor(item).organization"> · {{ translationFor(item).organization }}</span>
        </v-list-item-subtitle>
        <template #append>
          <v-btn icon="mdi-pencil" variant="text" aria-label="Редактировать достижение" @click="openEditor(item)" />
          <v-btn icon="mdi-delete" variant="text" color="error" aria-label="Удалить достижение" @click="pendingDelete = item" />
        </template>
      </v-list-item>
    </v-list>
    <v-alert v-else-if="!loading" type="info" variant="tonal">Достижения пока не добавлены.</v-alert>

    <v-dialog v-model="editorOpen" max-width="800" persistent>
      <v-card>
        <v-card-title>{{ editing ? 'Редактировать достижение' : 'Новое достижение' }}</v-card-title>
        <v-card-text><AchievementForm ref="formRef" v-model="form" /></v-card-text>
        <v-card-actions class="justify-end">
          <v-btn @click="editorOpen = false">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" @click="save">{{ editing ? 'Сохранить' : 'Создать' }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog :model-value="!!pendingDelete" max-width="420" @update:model-value="value => !value && (pendingDelete = null)">
      <v-card>
        <v-card-title>Удалить достижение?</v-card-title>
        <v-card-text>{{ translationFor(pendingDelete || {}).title }}</v-card-text>
        <v-card-actions class="justify-end">
          <v-btn @click="pendingDelete = null">Отмена</v-btn>
          <v-btn color="error" :loading="deleting" @click="remove">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import AchievementForm from '@/components/achievements/AchievementForm.vue'
import { useAchievementStore } from '@/stores/achievement'

const store = useAchievementStore()
const { locale } = useI18n()
const achievements = ref([])
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const error = ref('')
const editorOpen = ref(false)
const editing = ref(false)
const form = ref({})
const formRef = ref(null)
const pendingDelete = ref(null)

const categoryLabels = {
  grant: 'Грант', award: 'Награда', certification: 'Сертификация',
  competition: 'Конкурс', research: 'Исследование', expertise: 'Экспертная деятельность',
}
const scopeLabels = { personal: 'Личное', team: 'Командное', students: 'Ученики' }

function translationFor(item) {
  return item.translations?.find((translation) => translation.lang === locale.value)
    || item.translations?.find((translation) => translation.lang === 'ru')
    || item.translations?.[0]
    || {}
}
function categoryLabel(value) { return categoryLabels[value] || value }
function scopeLabel(value) { return scopeLabels[value] || value }

async function load() {
  loading.value = true
  error.value = ''
  const data = await store.loadAdminAchievements({ params: { offset: 0, limit: 100 } })
  if (data?.items) achievements.value = data.items
  else error.value = 'Не удалось загрузить достижения.'
  loading.value = false
}

function openEditor(item = null) {
  editing.value = !!item
  form.value = item ? JSON.parse(JSON.stringify(item)) : {}
  editorOpen.value = true
}

async function save() {
  if (!(await formRef.value?.submit())) return
  saving.value = true
  error.value = ''
  const { id, created_at, updated_at, ...payload } = form.value
  payload.year = payload.year === '' || payload.year == null ? null : Number(payload.year)
  payload.order = Number(payload.order || 0)
  payload.source_url = payload.source_url || null
  payload.image_url = payload.image_url || null
  payload.translations = (payload.translations || []).map(({ lang, title, organization, result, short_description, description }) => ({
    lang, title, organization: organization || null, result: result || null,
    short_description: short_description || null, description: description || null,
  }))
  const result = editing.value
    ? await store.updateAchievement(id, payload)
    : await store.createAchievement(payload)
  saving.value = false
  if (!result) { error.value = 'Не удалось сохранить достижение.'; return }
  editorOpen.value = false
  await load()
}

async function remove() {
  if (!pendingDelete.value) return
  deleting.value = true
  const result = await store.deleteAchievement(pendingDelete.value.id)
  deleting.value = false
  if (!result) { error.value = 'Не удалось удалить достижение.'; return }
  pendingDelete.value = null
  await load()
}

onMounted(load)
</script>
