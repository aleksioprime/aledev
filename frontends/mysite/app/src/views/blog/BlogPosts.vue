<template>
  <v-container>
    <v-row class="mb-4">
      <v-col cols="12" md="8">
        <h1 class="text-h3 mb-2">Все посты</h1>
        <p class="text-subtitle-1">Управление постами блога</p>
      </v-col>
      <v-col cols="12" md="4" class="text-md-end">
        <v-btn color="success" variant="elevated" :to="{ name: 'blog-post-create' }" v-if="canEdit">
          <v-icon start>mdi-plus</v-icon>
          Создать пост
        </v-btn>
      </v-col>
    </v-row>

    <!-- Поиск и фильтры -->
    <v-row class="mb-6">
      <v-col cols="12" md="6">
        <v-text-field v-model="searchQuery" label="Поиск постов" prepend-inner-icon="mdi-magnify" variant="outlined"
          density="compact" clearable @input="debouncedSearch" />
      </v-col>
      <v-col cols="12" md="3">
        <v-select v-model="selectedCategory" :items="categories" label="Категория" variant="outlined" density="compact"
          clearable @update:model-value="filterPosts" />
      </v-col>
      <v-col cols="12" md="3">
        <v-select v-model="sortBy" :items="sortOptions" label="Сортировка" variant="outlined" density="compact"
          @update:model-value="filterPosts" />
      </v-col>
    </v-row>

    <!-- Алерт для ошибок -->
    <v-alert v-if="postStore.hasError" type="error" variant="tonal" class="mb-4" closable
      @click:close="postStore.clearError()">
      {{ postStore.error }}
    </v-alert>

    <!-- Список постов -->
    <div v-if="!postStore.isLoading">
      <div v-if="filteredPosts.length">
        <v-card v-for="post in filteredPosts" :key="post.id" class="mb-4" hover>
          <v-card-title class="d-flex justify-space-between align-center">
            <router-link :to="{ name: 'blog-post', params: { slug: post.slug } }"
              class="text-decoration-none flex-grow-1">
              {{ post.title }}
            </router-link>
            <div class="d-flex gap-2">
              <v-btn :to="{ name: 'blog-post-edit', params: { id: post.id } }" icon="mdi-pencil" size="small"
                variant="text" color="primary" />
              <v-btn @click="confirmDelete(post)" icon="mdi-delete" size="small" variant="text" color="error" />
            </div>
          </v-card-title>

          <v-card-subtitle>
            <v-chip size="small" class="me-2">
              <v-icon start size="small">mdi-calendar</v-icon>
              {{ formatDate(post.created_at) }}
            </v-chip>
            <v-chip v-if="post.category" size="small" color="primary" variant="outlined">
              {{ post.category }}
            </v-chip>
            <v-chip :color="post.published ? 'success' : 'warning'" size="small" class="ms-2">
              {{ post.published ? 'Опубликован' : 'Черновик' }}
            </v-chip>
          </v-card-subtitle>

          <v-card-text>
            <p>{{ truncateText(post.description || post.content, 200) }}</p>
          </v-card-text>

          <v-card-actions>
            <v-btn :to="{ name: 'blog-post', params: { slug: post.slug } }" variant="text" color="primary">
              Просмотр
            </v-btn>
            <v-btn :to="{ name: 'blog-post-edit', params: { id: post.id } }" variant="text" color="primary">
              Редактировать
            </v-btn>
            <v-spacer />
            <v-btn @click="confirmDelete(post)" variant="text" color="error">
              Удалить
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>

      <v-alert v-else type="info" variant="tonal">
        <div v-if="searchQuery || selectedCategory">
          По вашему запросу ничего не найдено.
        </div>
        <div v-else>
          Пока нет созданных постов.
          <router-link :to="{ name: 'blog-post-create' }">Создать первый пост</router-link>
        </div>
      </v-alert>
    </div>

    <!-- Скелетон загрузки -->
    <v-skeleton-loader v-else type="card, card, card" class="mb-4" />

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog.show" max-width="500">
      <v-card>
        <v-card-title>
          <v-icon class="me-2" color="error">mdi-delete-alert</v-icon>
          Подтверждение удаления
        </v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить пост "<strong>{{ deleteDialog.post?.title }}</strong>"?
          <br>
          <small class="text-error">Это действие нельзя отменить.</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="deleteDialog.show = false" variant="text">
            Отмена
          </v-btn>
          <v-btn @click="deletePost" color="error" variant="elevated" :loading="deleteDialog.loading">
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Снекбар для уведомлений -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
      <template #actions>
        <v-btn @click="snackbar.show = false" icon="mdi-close" />
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'

import { format } from 'date-fns'
import { ru } from 'date-fns/locale'

import { useAuthStore } from "@/stores/auth"
const authStore = useAuthStore()

const canEdit = computed(() => authStore.isSuperuser)

import { usePostStore } from '@/stores/post'
const postStore = usePostStore()

// Поиск и фильтрация
const searchQuery = ref('')
const selectedCategory = ref(null)
const sortBy = ref('created_at:desc')

// Опции для селектов
const categories = ref(['Программирование', 'Веб-разработка', 'Инструменты', 'Личное'])
const sortOptions = ref([
  { title: 'Сначала новые', value: 'created_at:desc' },
  { title: 'Сначала старые', value: 'created_at:asc' },
  { title: 'По алфавиту', value: 'title:asc' },
  { title: 'По алфавиту (обратно)', value: 'title:desc' }
])

// Диалог удаления
const deleteDialog = ref({
  show: false,
  post: null,
  loading: false
})

// Снекбар
const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

// Вычисляемые свойства
const filteredPosts = computed(() => {
  let posts = [...postStore.posts]

  // Поиск по заголовку и содержимому
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    posts = posts.filter(post =>
      post.title.toLowerCase().includes(query) ||
      (post.description && post.description.toLowerCase().includes(query)) ||
      (post.content && post.content.toLowerCase().includes(query))
    )
  }

  // Фильтр по категории
  if (selectedCategory.value) {
    posts = posts.filter(post => post.category === selectedCategory.value)
  }

  // Сортировка
  const [field, order] = sortBy.value.split(':')
  posts.sort((a, b) => {
    let aValue = a[field]
    let bValue = b[field]

    if (field === 'created_at') {
      aValue = new Date(aValue)
      bValue = new Date(bValue)
    }

    if (order === 'desc') {
      return bValue > aValue ? 1 : -1
    } else {
      return aValue > bValue ? 1 : -1
    }
  })

  return posts
})

// Методы
const formatDate = (date) => {
  return format(new Date(date), 'dd MMMM yyyy', { locale: ru })
}

const truncateText = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

let searchTimeout = null
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    filterPosts()
  }, 300)
}

const filterPosts = () => {
  // Фильтрация происходит через computed свойство
}

const confirmDelete = (post) => {
  deleteDialog.value.post = post
  deleteDialog.value.show = true
}

const deletePost = async () => {
  deleteDialog.value.loading = true

  try {
    const success = await postStore.deletePost(deleteDialog.value.post.id)

    if (success) {
      showSnackbar('Пост успешно удален', 'success')
      deleteDialog.value.show = false
    } else {
      showSnackbar('Ошибка при удалении поста', 'error')
    }
  } catch (error) {
    showSnackbar('Ошибка при удалении поста', 'error')
  } finally {
    deleteDialog.value.loading = false
  }
}

const showSnackbar = (text, color = 'success') => {
  snackbar.value.text = text
  snackbar.value.color = color
  snackbar.value.show = true
}

onMounted(async () => {
  await postStore.loadPosts()
})
</script>