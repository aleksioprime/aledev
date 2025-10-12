<template>
  <div class="blog-home">
    <!-- Hero секция -->
    <v-container fluid class="hero-section pa-0">
      <v-row no-gutters class="fill-height">
        <v-col cols="12">
          <div class="hero-content text-center pa-8">
            <h1 class="display-1 font-weight-bold mb-4">
              Добро пожаловать в AleBlog
            </h1>
            <p class="headline mb-6">
              Личный блог Алексея Семочкина о разработке, технологиях и жизни
            </p>
            <v-btn color="primary" size="large" rounded @click="$router.push('/posts')" class="mr-4">
              Читать посты
            </v-btn>
            <v-btn variant="outlined" size="large" rounded @click="$router.push('/about')">
              О блоге
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>

    <!-- Последние посты -->
    <v-container class="my-12">
      <h2 class="text-h4 mb-8 text-center">Последние посты</h2>
      <v-row>
        <v-col v-for="post in latestPosts" :key="post.id" cols="12" md="6" lg="4">
          <blog-post-card :post="post" />
        </v-col>
      </v-row>

      <div class="text-center mt-8">
        <v-btn color="primary" variant="outlined" @click="$router.push('/posts')">
          Смотреть все посты
        </v-btn>
      </div>
    </v-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BlogPostCard from '@/components/blog/BlogPostCard.vue'


onMounted(() => {

})
</script>

<style scoped></style>