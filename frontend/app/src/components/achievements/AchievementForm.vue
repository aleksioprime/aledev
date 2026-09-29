<template>
  <v-form ref="formRef" @submit.prevent="submit">
    <v-row>
      <v-col cols="12" sm="6">
        <v-select v-model="form.category" label="Категория" :items="categoryItems" item-title="title" item-value="value" />
      </v-col>
      <v-col cols="12" sm="6">
        <v-select v-model="form.scope" label="Кто достиг результата" :items="scopeItems" item-title="title" item-value="value" />
      </v-col>
      <v-col cols="12" sm="4">
        <v-text-field v-model.number="form.year" label="Год" type="number" min="1900" max="2200" clearable />
      </v-col>
      <v-col cols="12" sm="8">
        <v-text-field v-model="form.source_url" label="Ссылка на источник или подтверждение" />
      </v-col>
      <v-col cols="12">
        <v-text-field v-model="form.image_url" label="Ссылка на изображение (необязательно)" />
      </v-col>
      <v-col cols="12" sm="4">
        <v-text-field v-model.number="form.order" label="Порядок" type="number" min="0" />
      </v-col>
      <v-col cols="12" sm="4"><v-switch v-model="form.is_featured" label="Избранное" color="primary" /></v-col>
      <v-col cols="12" sm="4"><v-switch v-model="form.is_published" label="Опубликовано" color="primary" /></v-col>
    </v-row>

    <v-tabs v-model="currentLang" bg-color="grey-lighten-4" grow class="mb-3">
      <v-tab v-for="translation in form.translations" :key="translation.lang" :value="translation.lang">
        {{ LANGS[translation.lang] || translation.lang.toUpperCase() }}
      </v-tab>
    </v-tabs>
    <div v-for="translation in form.translations" :key="translation.lang" v-show="currentLang === translation.lang">
      <v-text-field v-model="translation.title" :label="`Название (${LANGS[translation.lang]})`"
        :rules="[value => !!value?.trim() || 'Название обязательно']" required />
      <v-text-field v-model="translation.organization" :label="`Организатор (${LANGS[translation.lang]})`" />
      <v-text-field v-model="translation.result" :label="`Результат (${LANGS[translation.lang]})`" />
      <v-textarea v-model="translation.short_description" :label="`Краткое описание (${LANGS[translation.lang]})`" rows="2" auto-grow counter="500" />
      <v-textarea v-model="translation.description" :label="`Подробности (${LANGS[translation.lang]})`" rows="3" auto-grow />
    </div>
  </v-form>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { LANGS } from '@/common/constants/langs'

const props = defineProps({ modelValue: { type: Object, default: () => ({}) } })
const emit = defineEmits(['update:modelValue'])

const categoryItems = [
  { title: 'Грант', value: 'grant' },
  { title: 'Награда', value: 'award' },
  { title: 'Сертификация', value: 'certification' },
  { title: 'Конкурс', value: 'competition' },
  { title: 'Исследование', value: 'research' },
  { title: 'Экспертная деятельность', value: 'expertise' },
]
const scopeItems = [
  { title: 'Личное достижение', value: 'personal' },
  { title: 'Командный результат', value: 'team' },
  { title: 'Результат учеников', value: 'students' },
]

const blankTranslation = (lang) => ({
  lang,
  title: '',
  organization: '',
  result: '',
  short_description: '',
  description: '',
})
const defaults = () => ({
  category: 'competition',
  scope: 'personal',
  year: new Date().getFullYear(),
  source_url: '',
  image_url: '',
  order: 0,
  is_featured: false,
  is_published: true,
  translations: [blankTranslation('ru'), blankTranslation('en')],
})
const form = reactive(defaults())
const currentLang = ref('ru')
const formRef = ref(null)

watch(() => props.modelValue, (value) => {
  Object.assign(form, defaults(), value || {})
  form.translations = value?.translations?.length
    ? value.translations.map((translation) => ({ ...blankTranslation(translation.lang), ...translation }))
    : defaults().translations
  currentLang.value = form.translations[0]?.lang || 'ru'
}, { immediate: true })

watch(form, (value) => emit('update:modelValue', { ...value, translations: value.translations.map((item) => ({ ...item })) }), { deep: true })


async function submit() {
  return (await formRef.value?.validate())?.valid ?? false
}

defineExpose({ submit })
</script>
