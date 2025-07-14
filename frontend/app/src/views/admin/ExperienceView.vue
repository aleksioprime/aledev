<template>
  <div>
    <h1 class="text-h5 mb-4">Опыт работы</h1>

    <div class="d-flex align-top justify-space-between">
      <v-btn v-if="canEdit" color="primary" class="my-2" @click="openEditDialog()">
        <v-icon start>mdi-plus</v-icon>
        Добавить
      </v-btn>
    </div>

    <v-list class="pa-0 mt-4">
      <v-list-item v-for="experience in experiences" :key="experience.id">
        <v-list-item-title>
          {{ getExperienceTitle(experience) }}
        </v-list-item-title>
        <v-list-item-subtitle>
          {{ getExperienceTranslation(experience).responsibilities }}
        </v-list-item-subtitle>
        <template #append>
          <template v-if="canEdit">
            <v-btn icon @click.stop="openEditDialog(experience)" class="me-2">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon @click.stop="deleteExperience(experience)">
              <v-icon color="red">mdi-delete</v-icon>
            </v-btn>
          </template>
        </template>
      </v-list-item>
    </v-list>

    <div ref="infiniteScrollTarget" />

    <div class="text-center my-4" v-if="loading">
      <v-progress-circular indeterminate color="primary" />
    </div>

    <div class="text-center my-4" v-if="!loading && !hasNextPage && experiences.length">
      <v-alert type="info" density="compact" border="start" variant="tonal">
        Весь опыт загружен
      </v-alert>
    </div>

    <v-alert v-if="!experiences.length" type="info" class="mt-4">
      Опыт работы пока не добавлен
    </v-alert>

    <!-- Модальное окно добавления/редактирования -->
    <v-dialog v-model="modalDialogEdit.visible" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          {{ modalDialogEdit.editing ? 'Редактировать опыт' : 'Новый опыт' }}
        </v-card-title>
        <v-card-text>
          <ExperienceForm ref="experienceFormRef" v-model="modalDialogEdit.form" />
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn @click="modalDialogEdit.visible = false">Отмена</v-btn>
          <v-btn color="primary" @click="submitDialog">
            {{ modalDialogEdit.editing ? 'Сохранить' : 'Создать' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Модальное окно удаления -->
    <v-dialog v-model="modalDialogDelete.visible" max-width="400px">
      <v-card>
        <v-card-title>Удалить опыт?</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить
          <strong>{{ getExperienceTitle(modalDialogDelete.experience || {}) }}</strong>?
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn @click="modalDialogDelete.visible = false">Отмена</v-btn>
          <v-btn color="red" @click="confirmDeleteExperience">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useIntersectionObserver } from "@vueuse/core";
import { format } from "date-fns";
import ru from "date-fns/locale/ru";

import { useI18n } from 'vue-i18n'
const { locale } = useI18n()

import ExperienceForm from "@/components/experiences/ExperienceForm.vue";

import { useExperienceStore } from "@/stores/experience";
const experienceStore = useExperienceStore();
const experiences = ref([]);

import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();

function getExperienceTranslation(experience) {
  return experience.translations?.find(t => t.lang === locale.value)
    || experience.translations?.[0]
    || {};
}

function getExperienceTitle(experience) {
  const tr = getExperienceTranslation(experience);
  if (!tr) return "Без данных";
  if (tr.position && tr.company) return `${tr.position}, ${tr.company}`;
  if (tr.position) return tr.position;
  if (tr.company) return tr.company;
  return "Без данных";
}

function getExperienceDescription(experience) {
  return getExperienceTranslation(experience).description || "";
}

const canEdit = (experience) => {
  return (
    authStore.isSuperuser
  );
};

// --- СПИСОК ПРОЕКТОВ ---

// Переменные пагинированного списка
const page = ref(0);
const limit = 20;
const total = ref(0);
const hasNextPage = ref(true);

// Переменная процесса загрузки
const loading = ref(false);

// Загрузка пагинированного списка
const fetchExperiences = async (reset = false) => {
  if (loading.value) return;
  loading.value = true;

  // Если изменился фильтр или нужно перезагрузить весь список:
  if (reset) {
    experiences.value = [];
    page.value = 0;
    hasNextPage.value = true;
  }

  // Формируем параметры запроса для API
  const params = {
    offset: page.value,
    limit,
  };

  // Запрос к API с передачей параметров
  const data = await experienceStore.loadExperiences({ params: params });

  // Если данные получены
  if (data) {
    experiences.value.push(...data.items);
    total.value = data.total;
    hasNextPage.value = data.has_next;
    page.value += 1;
  }

  loading.value = false;
};

// Элемент страницы, который активирует подзагрузку списка
const infiniteScrollTarget = ref(null);

// Хук, который следит, попал ли элемент подзагрузки списка в поле видимости
useIntersectionObserver(
  infiniteScrollTarget,
  ([{ isIntersecting }]) => {
    if (isIntersecting) {
      fetchExperiences();
    }
  },
  {
    threshold: 1.0,
  }
);

// --- ДОБАВЛЕНИЕ/РЕДАКТИРОВАНИЕ ПРОЕКТОВ ---

// Объект модального окна
const modalDialogEdit = ref({
  visible: false,
  editing: false,
  form: {},
});

// Открытие модального окна для создания/редактирования проекта
const toDateInput = (val) => (val ? val.slice(0, 10) : null);

const openEditDialog = (experience = null) => {
  modalDialogEdit.value = {
    visible: true,
    editing: !!experience,
    form: experience
      ? {
        ...JSON.parse(JSON.stringify(experience)),
        start_date: toDateInput(experience.start_date),
        end_date: toDateInput(experience.end_date),
      }
      : {
        start_date: '',
        end_date: '',
        is_current: false,
        translations: [
          { lang: "ru", position: "", company: "", responsibilities: "", description: "" },
          { lang: "en", position: "", company: "", responsibilities: "", description: "" }
        ]
      }
  };
};

// Подготовка данных формы для запроса создания/редактирования проектов
function getFormPayload(form) {
  const { id, created_at, updated_at, ...data } = form;
  data.translations = (data.translations || []).map(
    ({ lang, position, company, responsibilities, description }) => ({
      lang, position, company, responsibilities, description
    })
  );
  return data;
}

// Подтверждение создания/редактирования проекта
const experienceFormRef = ref();

const submitDialog = async () => {
  const valid = await experienceFormRef.value?.submit();
  if (!valid) return;

  const { form, editing } = modalDialogEdit.value;
  const payload = getFormPayload(form);

  if (editing) {
    const result = await experienceStore.updateExperience(form.id, payload);
    if (!result) return;

    const index = experiences.value.findIndex(p => p.id === form.id);
    if (index !== -1) experiences.value[index] = { ...experiences.value[index], ...form };

  } else {
    const newExperience = await experienceStore.createExperience(payload);
    if (!newExperience) return;

    await fetchExperiences(true);
  }

  modalDialogEdit.value.visible = false;
};

// --- УДАЛЕНИЕ ПАЦИЕНТА ---

// Объект модального окна
const modalDialogDelete = ref({
  visible: false,
  experience: null,
});

// Вызов модального окна удаления
const deleteExperience = (experience) => {
  modalDialogDelete.value = {
    visible: true,
    experience,
  };
};

// Подтверждение удаления в модальном окне
const confirmDeleteExperience = async () => {
  const experience = modalDialogDelete.value.experience;

  const result = await experienceStore.deleteExperience(experience.id);
  if (!result) return;

  experiences.value = experiences.value.filter((p) => p.id !== experience.id);
  modalDialogDelete.value.visible = false;
};



const formatDate = (dateStr) => {
  return format(new Date(dateStr), "d MMMM yyyy", { locale: ru });
};

</script>