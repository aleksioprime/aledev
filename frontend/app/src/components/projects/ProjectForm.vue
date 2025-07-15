<template>
  <v-form ref="formRef" @submit.prevent="onSubmit">
    <!-- Базовые поля проекта -->
    <div class="flex ">
      <v-checkbox v-model="useOrder" label="Задать порядок вручную" />
    <v-text-field v-if="useOrder" v-model="form.order" label="Порядок" type="number" min="0"
      hint="0 — первый, 1 — второй и т.д." persistent-hint class="ms-5" />
    </div>

    <v-text-field v-model="form.stack" label="Технологический стек" />
    <v-text-field v-model="form.link" label="Ссылка на проект" />
    <v-text-field v-model="form.github_url" label="GitHub" />
    <v-text-field v-model="form.demo_url" label="Demo" />

    <v-checkbox v-model="form.is_favorite" label="Избранный проект" class="mb-2" />

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
      <v-text-field v-model="t.title" :label="`Название (${LANGS[t.lang]})`" :rules="[rules.required]" required />
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

const useOrder = ref(false);

// Базовое состояние формы
const blankTranslation = lang => ({ lang, title: "", description: "" });
const form = reactive({
  stack: "",
  link: "",
  github_url: "",
  demo_url: "",
  is_favorite: false,
  order: null,
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

// --- watch: внешние данные в форму ---
watch(
  () => props.modelValue,
  (val) => {
    if (!val) return;
    Object.assign(form, { ...val });
    // если translations пусты, создаём дефолтные
    if (!form.translations || form.translations.length === 0) {
      form.translations = [blankTranslation("ru")];
    }
    // активируем первый язык
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

// Валидация
const formRef = ref();
const onSubmit = async () => {
  const { valid } = await formRef.value?.validate();
  return valid;
};

defineExpose({ submit: onSubmit });
</script>