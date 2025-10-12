<template>
  <v-container>
    <div v-if="!postStore.isLoading && post">
      <!-- Хлебные крошки -->
      <v-breadcrumbs class="px-0">
        <v-breadcrumbs-item :to="{ name: 'blog-home' }">
          Главная
        </v-breadcrumbs-item>
        <v-breadcrumbs-item :to="{ name: 'blog-posts' }">
          Посты
        </v-breadcrumbs-item>
        <v-breadcrumbs-item>
          {{ post.title }}
        </v-breadcrumbs-item>
      </v-breadcrumbs>

      <!-- Заголовок поста -->
      <div class="mb-6">
        <h1 class="text-h3 mb-4">{{ post.title }}</h1>

        <div class="d-flex flex-wrap align-center gap-2 mb-4">
          <v-chip color="primary" variant="tonal">
            <v-icon start>mdi-calendar</v-icon>
            {{ formatDate(post.created_at) }}
          </v-chip>

          <v-chip v-if="post.category" color="secondary" variant="outlined">
            <v-icon start>mdi-tag</v-icon>
            {{ post.category }}
          </v-chip>

          <v-chip
            :color="post.published ? 'success' : 'warning'"
            variant="tonal"
          >
            <v-icon start>{{ post.published ? 'mdi-eye' : 'mdi-eye-off' }}</v-icon>
            {{ post.published ? 'Опубликован' : 'Черновик' }}
          </v-chip>

          <v-chip v-if="post.updated_at && post.updated_at !== post.created_at" variant="outlined">
            <v-icon start>mdi-pencil</v-icon>
            Обновлен {{ formatDate(post.updated_at) }}
          </v-chip>
        </div>

        <!-- Кнопки управления -->
        <div class="d-flex gap-2 mb-4">
          <v-btn
            :to="{ name: 'blog-post-edit', params: { id: post.id } }"
            color="primary"
            variant="elevated"
          >
            <v-icon start>mdi-pencil</v-icon>
            Редактировать
          </v-btn>

          <v-btn
            @click="confirmDelete"
            color="error"
            variant="outlined"
          >
            <v-icon start>mdi-delete</v-icon>
            Удалить
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

      <!-- Описание поста -->
      <v-card v-if="post.description" class="mb-6">
        <v-card-text>
          <div class="text-h6 mb-2">Описание</div>
          <p class="text-body-1">{{ post.description }}</p>
        </v-card-text>
      </v-card>

      <!-- Содержимое поста -->
      <v-card>
        <v-card-text>
          <div class="post-content" v-html="formattedContent"></div>
        </v-card-text>
      </v-card>

      <!-- Информация о посте -->
      <v-card class="mt-6">
        <v-card-title>
          <v-icon class="me-2">mdi-information</v-icon>
          Информация о посте
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" sm="6">
              <div class="text-subtitle-2">ID поста</div>
              <div class="text-body-2">{{ post.id }}</div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-subtitle-2">Slug</div>
              <div class="text-body-2">{{ post.slug }}</div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-subtitle-2">Создан</div>
              <div class="text-body-2">{{ formatDateTime(post.created_at) }}</div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="text-subtitle-2">Обновлен</div>
              <div class="text-body-2">{{ formatDateTime(post.updated_at) }}</div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </div>

    <!-- Загрузка -->
    <div v-else-if="postStore.isLoading">
      <v-skeleton-loader type="breadcrumbs" class="mb-4" />
      <v-skeleton-loader type="heading" class="mb-4" />
      <v-skeleton-loader type="chip, chip, chip" class="mb-4" />
      <v-skeleton-loader type="button, button, button" class="mb-6" />
      <v-skeleton-loader type="card" />
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

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title>
          <v-icon class="me-2" color="error">mdi-delete-alert</v-icon>
          Подтверждение удаления
        </v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить пост "<strong>{{ post?.title }}</strong>"?
          <br>
          <small class="text-error">Это действие нельзя отменить.</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            @click="deleteDialog = false"
            variant="text"
          >
            Отмена
          </v-btn>
          <v-btn
            @click="deletePost"
            color="error"
            variant="elevated"
            :loading="deleteLoading"
          >
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePostStore } from '@/stores/post'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'

const route = useRoute()
const router = useRouter()
const postStore = usePostStore()

const deleteDialog = ref(false)
const deleteLoading = ref(false)
const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const post = computed(() => postStore.currentPost)

// Форматированный контент с базовой HTML-разметкой
const formattedContent = computed(() => {
  if (!post.value?.content) return ''

  // Простое преобразование переносов строк в <br>
  return post.value.content
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
    .replace(/^/, '<p>')
    .replace(/$/, '</p>')
})

const formatDate = (date) => {
  return format(new Date(date), 'dd MMMM yyyy', { locale: ru })
}

const formatDateTime = (date) => {
  return format(new Date(date), 'dd MMMM yyyy, HH:mm', { locale: ru })
}

const confirmDelete = () => {
  deleteDialog.value = true
}

const deletePost = async () => {
  deleteLoading.value = true

  try {
    const success = await postStore.deletePost(post.value.id)

    if (success) {
      showSnackbar('Пост успешно удален', 'success')
      deleteDialog.value = false

      // Перенаправляем на список постов через небольшую задержку
      setTimeout(() => {
        router.push({ name: 'blog-posts' })
      }, 1000)
    } else {
      showSnackbar('Ошибка при удалении поста', 'error')
    }
  } catch (error) {
    showSnackbar('Ошибка при удалении поста', 'error')
  } finally {
    deleteLoading.value = false
  }
}

const showSnackbar = (text, color = 'success') => {
  snackbar.value.text = text
  snackbar.value.color = color
  snackbar.value.show = true
}

onMounted(async () => {
  const slug = route.params.slug
  if (slug) {
    await postStore.loadPost(slug)
  }
})
</script>

<style scoped>
.post-content {
  line-height: 1.7;
}

.post-content :deep(p) {
  margin-bottom: 1rem;
}

.post-content :deep(h1),
.post-content :deep(h2),
.post-content :deep(h3),
.post-content :deep(h4),
.post-content :deep(h5),
.post-content :deep(h6) {
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.post-content :deep(ul),
.post-content :deep(ol) {
  margin-bottom: 1rem;
  padding-left: 2rem;
}

.post-content :deep(blockquote) {
  border-left: 4px solid #1976d2;
  padding-left: 1rem;
  margin: 1rem 0;
  font-style: italic;
  color: rgba(0, 0, 0, 0.6);
}

.post-content :deep(code) {
  background-color: #f5f5f5;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
}
</style>