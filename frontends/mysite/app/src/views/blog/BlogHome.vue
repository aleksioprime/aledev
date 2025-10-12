<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div class="text-center mb-8">
          <h1 class="text-h2 mb-4">Блог разработчика</h1>
          <p class="text-h6 font-weight-light"></p>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card class="mb-6">
          <v-card-title>
            <h2>Добро пожаловать </h2>
          </v-card-title>
          <v-card-text>
            <p>
              Здесь я делюсь своими мыслями о разработке, технологиях и жизни.
              Вы найдете статьи о программировании, веб-разработке, инструментах разработчика и многом другом.
            </p>
            <v-btn color="primary" variant="elevated" :to="{ name: 'blog-posts' }" class="mt-4">
              <v-icon start>mdi-book-open-page-variant</v-icon>
              Читать посты
            </v-btn>
          </v-card-text>
        </v-card>

        <!-- Последние посты -->
        <div v-if="!postStore.isLoading">
          <h3 class="text-h4 mb-4">Последние посты</h3>
          <div v-if="recentPosts.length">
            <v-card v-for="post in recentPosts" :key="post.id" class="mb-4" hover>
              <v-card-title>
                <router-link :to="{ name: 'blog-post', params: { slug: post.slug } }" class="text-decoration-none">
                  {{ post.title }}
                </router-link>
              </v-card-title>
              <v-card-subtitle>
                <v-chip size="small" class="me-2">
                  <v-icon start size="small">mdi-calendar</v-icon>
                  {{ formatDate(post.created_at) }}
                </v-chip>
                <v-chip v-if="post.category" size="small" color="primary" variant="outlined">
                  {{ post.category }}
                </v-chip>
              </v-card-subtitle>
              <v-card-text>
                <p>{{ truncateText(post.description || post.content, 150) }}</p>
              </v-card-text>
              <v-card-actions>
                <v-btn :to="{ name: 'blog-post', params: { slug: post.slug } }" variant="text" color="primary">
                  Читать далее
                  <v-icon end>mdi-arrow-right</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </div>
          <v-alert v-else type="info" variant="tonal">
            Пока нет опубликованных постов.
          </v-alert>
        </div>

        <v-skeleton-loader v-else type="card, card, card" class="mb-4" />
      </v-col>

      <!-- Боковая панель -->
      <v-col cols="12" md="4" v-if="canEdit">
        <v-card class="mb-4">
          <v-card-title>
            <v-icon class="me-2">mdi-cog</v-icon>
            Управление
          </v-card-title>
          <v-card-text>
            <v-btn :to="{ name: 'blog-post-create' }" color="success" variant="elevated" block class="mb-2">
              <v-icon start>mdi-plus</v-icon>
              Создать пост
            </v-btn>
            <v-btn :to="{ name: 'blog-posts' }" color="primary" variant="outlined" block>
              <v-icon start>mdi-format-list-bulleted</v-icon>
              Все посты
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { usePostStore } from '@/stores/post'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'

import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();

const canEdit = computed(() => authStore.isSuperuser);

const postStore = usePostStore()
const recentPosts = computed(() => postStore.posts.slice(0, 3))


const formatDate = (date) => {
  return format(new Date(date), 'dd MMMM yyyy', { locale: ru })
}

const truncateText = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

onMounted(async () => {
  // Для демонстрации - если нет постов, загружаем демо-данные
  if (postStore.posts.length === 0) {
    await postStore.loadPosts({ limit: 3, sort: 'created_at:desc' })
  }
})
</script>

<style scoped></style>