<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <!-- Хлебные крошки -->
        <v-breadcrumbs class="px-0">
          <v-breadcrumbs-item :to="{ name: 'blog-home' }">
            Главная
          </v-breadcrumbs-item>
          <v-breadcrumbs-item :to="{ name: 'blog-posts' }">
            Посты
          </v-breadcrumbs-item>
          <v-breadcrumbs-item v-if="post">
            {{ post.title }}
          </v-breadcrumbs-item>
          <v-breadcrumbs-item>
            Редактировать
          </v-breadcrumbs-item>
        </v-breadcrumbs>

        <div class="d-flex justify-space-between align-center mb-6">
          <h1 class="text-h3">Редактировать пост</h1>
          <div class="d-flex gap-2">
            <v-btn
              v-if="post"
              :to="{ name: 'blog-post', params: { slug: post.slug } }"
              variant="text"
            >
              <v-icon start>mdi-eye</v-icon>
              Просмотр
            </v-btn>
            <v-btn
              :to="{ name: 'blog-posts' }"
              variant="text"
            >
              <v-icon start>mdi-arrow-left</v-icon>
              К списку постов
            </v-btn>
          </div>
        </div>
      </v-col>
    </v-row>

    <div v-if="!postStore.isLoading && post">
      <v-form @submit.prevent="updatePost" ref="form">
        <v-row>
          <v-col cols="12" md="8">
            <!-- Основная карточка с формой -->
            <v-card>
              <v-card-title>
                <v-icon class="me-2">mdi-file-document-edit</v-icon>
                Содержимое поста
              </v-card-title>
              <v-card-text>
                <v-text-field
                  v-model="postData.title"
                  label="Заголовок поста"
                  variant="outlined"
                  :rules="titleRules"
                  required
                  class="mb-4"
                />

                <v-text-field
                  v-model="postData.slug"
                  label="Slug (URL)"
                  variant="outlined"
                  :rules="slugRules"
                  hint="Изменение slug может нарушить существующие ссылки"
                  persistent-hint
                  class="mb-4"
                />

                <v-textarea
                  v-model="postData.description"
                  label="Краткое описание"
                  variant="outlined"
                  rows="3"
                  hint="Краткое описание поста для предварительного просмотра"
                  persistent-hint
                  class="mb-4"
                />

                <v-textarea
                  v-model="postData.content"
                  label="Содержимое поста"
                  variant="outlined"
                  rows="15"
                  :rules="contentRules"
                  required
                  hint="Основной текст поста. Поддерживается простая разметка"
                  persistent-hint
                />
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <!-- Настройки публикации -->
            <v-card class="mb-4">
              <v-card-title>
                <v-icon class="me-2">mdi-cog</v-icon>
                Настройки публикации
              </v-card-title>
              <v-card-text>
                <v-select
                  v-model="postData.category"
                  :items="categories"
                  label="Категория"
                  variant="outlined"
                  clearable
                  class="mb-4"
                />

                <v-switch
                  v-model="postData.published"
                  label="Опубликован"
                  color="success"
                  hide-details
                />

                <v-divider class="my-4" />

                <div class="text-subtitle-2 mb-2">Дополнительные теги</div>
                <v-combobox
                  v-model="postData.tags"
                  label="Теги"
                  variant="outlined"
                  multiple
                  chips
                  closable-chips
                  hint="Нажмите Enter для добавления тега"
                  persistent-hint
                />
              </v-card-text>
            </v-card>

            <!-- Информация о посте -->
            <v-card class="mb-4">
              <v-card-title>
                <v-icon class="me-2">mdi-information</v-icon>
                Информация
              </v-card-title>
              <v-card-text>
                <div class="text-subtitle-2">ID поста</div>
                <div class="text-body-2 mb-2">{{ post.id }}</div>

                <div class="text-subtitle-2">Создан</div>
                <div class="text-body-2 mb-2">{{ formatDateTime(post.created_at) }}</div>

                <div class="text-subtitle-2">Последнее обновление</div>
                <div class="text-body-2">{{ formatDateTime(post.updated_at) }}</div>
              </v-card-text>
            </v-card>

            <!-- Предварительный просмотр -->
            <v-card v-if="postData.title || postData.description">
              <v-card-title>
                <v-icon class="me-2">mdi-eye</v-icon>
                Предварительный просмотр
              </v-card-title>
              <v-card-text>
                <div class="preview-card">
                  <h3 class="text-h6 mb-2">{{ postData.title || 'Заголовок поста' }}</h3>
                  <div class="d-flex gap-2 mb-2">
                    <v-chip size="small" color="primary" variant="tonal">
                      <v-icon start size="small">mdi-calendar</v-icon>
                      {{ formatDate(post.created_at) }}
                    </v-chip>
                    <v-chip
                      v-if="postData.category"
                      size="small"
                      color="secondary"
                      variant="outlined"
                    >
                      {{ postData.category }}
                    </v-chip>
                    <v-chip
                      size="small"
                      :color="postData.published ? 'success' : 'warning'"
                      variant="tonal"
                    >
                      {{ postData.published ? 'Опубликован' : 'Черновик' }}
                    </v-chip>
                  </div>
                  <p class="text-body-2">
                    {{ truncateText(postData.description || postData.content, 100) }}
                  </p>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Кнопки действий -->
        <v-row class="mt-4">
          <v-col cols="12">
            <div class="d-flex justify-end gap-2">
              <v-btn
                :to="{ name: 'blog-post', params: { slug: post.slug } }"
                variant="text"
                :disabled="postStore.isLoading"
              >
                Отмена
              </v-btn>

              <v-btn
                @click="updatePost(false)"
                variant="outlined"
                color="primary"
                :loading="postStore.isLoading"
              >
                <v-icon start>mdi-content-save</v-icon>
                Сохранить как черновик
              </v-btn>

              <v-btn
                @click="updatePost(true)"
                color="success"
                variant="elevated"
                :loading="postStore.isLoading"
              >
                <v-icon start>mdi-publish</v-icon>
                {{ postData.published ? 'Обновить' : 'Опубликовать' }}
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-form>
    </div>

    <!-- Загрузка -->
    <div v-else-if="postStore.isLoading">
      <v-skeleton-loader type="breadcrumbs" class="mb-4" />
      <v-skeleton-loader type="heading" class="mb-6" />
      <v-row>
        <v-col cols="12" md="8">
          <v-skeleton-loader type="card" />
        </v-col>
        <v-col cols="12" md="4">
          <v-skeleton-loader type="card, card" />
        </v-col>
      </v-row>
    </div>

    <!-- Ошибка или пост не найден -->
    <v-alert
      v-else-if="postStore.hasError || !post"
      type="error"
      variant="tonal"
      class="mb-4"
    >
      <div v-if="postStore.hasError">
        {{ postStore.error }}
      </div>
      <div v-else>
        Пост не найден
      </div>
      <template #actions>
        <v-btn
          :to="{ name: 'blog-posts' }"
          variant="text"
        >
          К списку постов
        </v-btn>
      </template>
    </v-alert>

    <!-- Алерт для ошибок -->
    <v-alert
      v-if="postStore.hasError"
      type="error"
      variant="tonal"
      class="mt-4"
      closable
      @click:close="postStore.clearError()"
    >
      {{ postStore.error }}
    </v-alert>

    <!-- Снекбар для уведомлений -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      timeout="3000"
    >
      {{ snackbar.text }}
      <template #actions>
        <v-btn @click="snackbar.show = false" icon="mdi-close" />
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePostStore } from '@/stores/post'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'

const route = useRoute()
const router = useRouter()
const postStore = usePostStore()
const form = ref(null)

const post = computed(() => postStore.currentPost)

// Данные поста для редактирования
const postData = ref({
  title: '',
  slug: '',
  description: '',
  content: '',
  category: null,
  published: false,
  tags: []
})

// Категории для выбора
const categories = ref([
  'Программирование',
  'Веб-разработка',
  'Инструменты',
  'Личное',
  'Обучение',
  'Новости'
])

// Снекбар
const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

// Правила валидации
const titleRules = [
  v => !!v || 'Заголовок обязателен',
  v => (v && v.length >= 5) || 'Заголовок должен содержать минимум 5 символов',
  v => (v && v.length <= 200) || 'Заголовок не должен превышать 200 символов'
]

const slugRules = [
  v => !!v || 'Slug обязателен',
  v => /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(v) || 'Slug может содержать только строчные буквы, цифры и дефисы'
]

const contentRules = [
  v => !!v || 'Содержимое поста обязательно',
  v => (v && v.length >= 50) || 'Содержимое должно содержать минимум 50 символов'
]

// Заполняем форму данными из загруженного поста
watch(post, (newPost) => {
  if (newPost) {
    postData.value = {
      title: newPost.title || '',
      slug: newPost.slug || '',
      description: newPost.description || '',
      content: newPost.content || '',
      category: newPost.category || null,
      published: newPost.published || false,
      tags: newPost.tags || []
    }
  }
}, { immediate: true })

const formatDate = (date) => {
  return format(new Date(date), 'dd MMMM yyyy', { locale: ru })
}

const formatDateTime = (date) => {
  return format(new Date(date), 'dd MMMM yyyy, HH:mm', { locale: ru })
}

const truncateText = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

const updatePost = async (shouldPublish = null) => {
  // Валидируем форму
  const { valid } = await form.value.validate()
  if (!valid) {
    showSnackbar('Пожалуйста, исправьте ошибки в форме', 'error')
    return
  }

  // Устанавливаем статус публикации
  if (shouldPublish !== null) {
    postData.value.published = shouldPublish
  }

  try {
    const result = await postStore.updatePost(post.value.id, {
      ...postData.value,
      updated_at: new Date().toISOString()
    })

    if (result) {
      const message = postData.value.published
        ? 'Пост успешно обновлен и опубликован!'
        : 'Пост успешно обновлен!'

      showSnackbar(message, 'success')

      // Перенаправляем на страницу просмотра поста
      setTimeout(() => {
        router.push({
          name: 'blog-post',
          params: { slug: result.slug }
        })
      }, 1500)
    } else {
      showSnackbar('Ошибка при обновлении поста', 'error')
    }
  } catch (error) {
    showSnackbar('Ошибка при обновлении поста', 'error')
  }
}

const showSnackbar = (text, color = 'success') => {
  snackbar.value.text = text
  snackbar.value.color = color
  snackbar.value.show = true
}

onMounted(async () => {
  const postId = route.params.id
  if (postId) {
    await postStore.loadPost(postId)
  }
})
</script>

<style scoped>
.preview-card {
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 4px;
  padding: 16px;
  background-color: rgba(0, 0, 0, 0.02);
}
</style>