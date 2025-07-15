<template>
  <div>
    <h1 class="text-h5 mb-4">Проекты</h1>

    <div class="d-flex align-top justify-space-between">
      <v-btn v-if="canEdit" color="primary" class="my-2" @click="openEditDialog()">
        <v-icon start>mdi-plus</v-icon>
        Добавить
      </v-btn>
    </div>

    <v-list class="pa-0 mt-4">
      <v-list-item v-for="project in projects" :key="project.id">
        <v-list-item-title>
          {{ getProjectTitle(project) }}
        </v-list-item-title>
        <v-list-item-subtitle>
          {{ getProjectDescription(project) }}
        </v-list-item-subtitle>
        <v-list-item-subtitle v-if="project.stack">
          Технологии: {{ project.stack }}
        </v-list-item-subtitle>
        <v-list-item-subtitle v-if="project.github_url">
          <a :href="project.github_url" target="_blank">GitHub</a>
        </v-list-item-subtitle>
        <template #append>
          <template v-if="canEdit">
            <v-btn icon @click.stop="openEditDialog(project)" class="me-2">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon @click.stop="deleteProject(project)">
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

    <div class="text-center my-4" v-if="!loading && !hasNextPage && projects.length">
      <v-alert type="info" density="compact" border="start" variant="tonal">
        Все проекты загружены
      </v-alert>
    </div>

    <v-alert v-if="!projects.length" type="info" class="mt-4">
      Проекты пока не добавлены
    </v-alert>

    <!-- Модальное окно добавления/редактирования -->
    <v-dialog v-model="modalDialogEdit.visible" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          {{ modalDialogEdit.editing ? 'Редактировать проект' : 'Новый проект' }}
        </v-card-title>
        <v-card-text>
          <ProjectForm ref="projectFormRef" v-model="modalDialogEdit.form" />
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
        <v-card-title>Удалить проект?</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить проект
          <strong>{{ getProjectTitle(modalDialogDelete.project || {}) }}</strong>?
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn @click="modalDialogDelete.visible = false">Отмена</v-btn>
          <v-btn color="red" @click="confirmDeleteProject">Удалить</v-btn>
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

import ProjectForm from "@/components/projects/ProjectForm.vue";

import { useProjectStore } from "@/stores/project";
const projectStore = useProjectStore();
const projects = ref([]);

import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();

function getProjectTranslation(project) {
  return project.translations?.find(t => t.lang === locale.value)
    || project.translations?.[0]
    || {};
}

function getProjectTitle(project) {
  return getProjectTranslation(project).title || "Без названия";
}

function getProjectDescription(project) {
  return getProjectTranslation(project).description || "";
}

const canEdit = (project) => {
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
const fetchProjects = async (reset = false) => {
  if (loading.value) return;
  loading.value = true;

  // Если изменился фильтр или нужно перезагрузить весь список:
  if (reset) {
    projects.value = [];
    page.value = 0;
    hasNextPage.value = true;
  }

  // Формируем параметры запроса для API
  const params = {
    offset: page.value,
    limit,
  };

  // Запрос к API с передачей параметров
  const data = await projectStore.loadProjects({ params: params });

  // Если данные получены
  if (data) {
    projects.value.push(...data.items);
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
      fetchProjects();
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
const openEditDialog = (project = null) => {
  modalDialogEdit.value = {
    visible: true,
    editing: !!project,
    form: project
      ? JSON.parse(JSON.stringify(project)) // deep copy!
      : {
        stack: "",
        link: "",
        github_url: "",
        demo_url: "",
        is_favorite: false,
        translations: [
          { lang: "ru", title: "", description: "" },
          { lang: "en", title: "", description: "" }
        ]
      }
  };
};

// Подготовка данных формы для запроса создания/редактирования проектов
function getFormPayload(form) {
  // Только нужные поля и переводы
  const {
    id, created_at, updated_at, ...data
  } = form;
  data.translations = (data.translations || []).map(({ lang, title, description }) => ({
    lang, title, description
  }));
  return data;
}

// Подтверждение создания/редактирования проекта
const projectFormRef = ref();

const submitDialog = async () => {
  const valid = await projectFormRef.value?.submit();
  if (!valid) return;

  const { form, editing } = modalDialogEdit.value;
  const payload = getFormPayload(form);

  if (editing) {
    const result = await projectStore.updateProject(form.id, payload);
    if (!result) return;

    const index = projects.value.findIndex(p => p.id === form.id);
    if (index !== -1) projects.value[index] = { ...projects.value[index], ...form };

  } else {
    const newProject = await projectStore.createProject(payload);
    if (!newProject) return;

    await fetchProjects(true);
  }

  modalDialogEdit.value.visible = false;
};

// --- УДАЛЕНИЕ ПРОЕКТА ---

// Объект модального окна
const modalDialogDelete = ref({
  visible: false,
  project: null,
});

// Вызов модального окна удаления
const deleteProject = (project) => {
  modalDialogDelete.value = {
    visible: true,
    project,
  };
};

// Подтверждение удаления в модальном окне
const confirmDeleteProject = async () => {
  const project = modalDialogDelete.value.project;

  const result = await projectStore.deleteProject(project.id);
  if (!result) return;

  projects.value = projects.value.filter((p) => p.id !== project.id);
  modalDialogDelete.value.visible = false;
};



const formatDate = (dateStr) => {
  return format(new Date(dateStr), "d MMMM yyyy", { locale: ru });
};

</script>