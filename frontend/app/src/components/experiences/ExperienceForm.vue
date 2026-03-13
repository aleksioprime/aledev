<template>
  <v-form ref="formRef" @submit.prevent="onSubmit">
    <!-- Даты -->
    <v-row>
      <v-col cols="12" sm="6">
        <v-text-field v-model="form.start_date" label="Дата начала" type="date" :rules="[rules.required]" required />
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field v-model="form.end_date" label="Дата окончания" type="date" :disabled="form.is_current" />
      </v-col>
    </v-row>

    <!-- Текущая позиция -->
    <v-checkbox v-model="form.is_current" label="Текущее место работы" class="mb-2" />

    <!-- Переводы -->
    <div class="mb-2">
      <v-tabs v-model="currentLang" bg-color="grey-lighten-4" grow>
        <v-tab v-for="t in translationsList" :key="t.lang" :value="t.lang">
          {{ LANGS[t.lang] || t.lang.toUpperCase() }}
        </v-tab>
        <v-tab @click.prevent="addTranslation" :disabled="availableLangs.length === 0" value="add">
          + Добавить язык
        </v-tab>
      </v-tabs>
    </div>

    <div v-for="(t, idx) in form.translations" :key="t.lang" v-show="currentLang === t.lang">
      <v-text-field v-model="t.position" :label="`Должность (${LANGS[t.lang]})`" :rules="[rules.required]" required />
      <v-text-field v-model="t.company" :label="`Компания (${LANGS[t.lang]})`" :rules="[rules.required]" required />
      <v-textarea v-model="t.responsibilities" :label="`Краткие задачи (${LANGS[t.lang]})`" auto-grow />
      <v-textarea v-model="t.description" :label="`Описание (${LANGS[t.lang]})`" auto-grow />
      <v-btn v-if="form.translations.length > 1" variant="text" color="red" @click="removeTranslation(idx)" size="small"
        class="mt-0 mb-4">
        Удалить перевод
      </v-btn>
    </div>
  </v-form>
</template>

<script setup>
import { ref, reactive, watch, computed } from "vue";
import rules from "@/common/helpers/rules";

import { LANGS, LANG_ENUMS } from '@/common/constants/langs';

const props = defineProps({
  modelValue: Object,
});
const emit = defineEmits(["update:modelValue"]);

// Базовое состояние формы
const blankTranslation = lang => ({ lang, position: "", company: "", responsibilities: "", description: "" });
const form = reactive({
  start_date: "",
  end_date: null,
  is_current: false,
  translations: [blankTranslation("ru"), blankTranslation("en")]
});

// Список языков уже в переводах
const translationsList = computed(() => form.translations);

// Языки, которые ещё не добавлены
const availableLangs = computed(
  () => LANG_ENUMS.filter(l => !form.translations.find(t => t.lang === l))
);

// Активная вкладка языка
const currentLang = ref(form.translations[0].lang);

// Форматирование дат
const formatDate = (dateStr) => format(new Date(dateStr), "d MMMM yyyy", { locale: ru });

// --- watch: внешние данные в форму ---
watch(
  () => props.modelValue,
  (val) => {
    if (!val) return;
    Object.assign(form, { ...val });
    if (!form.translations || form.translations.length === 0) {
      form.translations = [blankTranslation("ru")];
    }
    currentLang.value = form.translations[0].lang;
  },
  { immediate: true }
);

// Синхронизация изменения внутренего modelValue с внешним
watch(
  () => ({ ...form }),
  val => emit("update:modelValue", val)
);

// Добавление перевода
function addTranslation() {
  if (availableLangs.value.length > 0) {
    const lang = availableLangs.value[0];
    form.translations.push(blankTranslation(lang));
    currentLang.value = lang;
  }
}

// Удаление перевода
function removeTranslation(idx) {
  if (form.translations.length > 1) {
    form.translations.splice(idx, 1);
    currentLang.value = form.translations[0].lang;
  }
}

// Если выбран is_current — обнуляем дату окончания
watch(() => form.is_current, val => {
  if (val) emit("update:modelValue", { ...form, end_date: null });
});

// Валидация
const formRef = ref();
const onSubmit = async () => {
  const { valid } = await formRef.value?.validate();
  return valid;
};

defineExpose({ submit: onSubmit });
</script>