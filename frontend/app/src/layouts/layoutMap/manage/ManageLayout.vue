<template>
  <!-- Навигационное меню (боковая панель) -->
  <v-navigation-drawer v-model="drawer" app :temporary="mobile" :width="240">
    <v-list>
      <!-- Заголовок меню -->
      <v-list-item>
        <v-list-item-title class="text-h6">Меню</v-list-item-title>
      </v-list-item>

      <!-- Разделитель -->
      <v-divider />

      <!-- Список пунктов меню -->
      <v-list-item v-for="item in menuItems" :key="item.title" :title="item.title" :prepend-icon="item.icon" link
        :to="{ name: item.to }" @click="handleMenuItemClick"/>
    </v-list>
  </v-navigation-drawer>

  <!-- Верхняя панель приложения -->
  <v-app-bar app color="primary" dark>
    <!-- Иконка открытия/закрытия боковой панели -->
    <v-app-bar-nav-icon @click="drawer = !drawer" />

    <!-- Логотип -->
    <v-img :src="admin" alt="Логотип" max-width="38" max-height="38" class="ms-2" />

    <!-- Заголовок -->
    <v-toolbar-title>
      <router-link :to="{ name: 'login' }" class="text-white text-decoration-none">
        Администраторская панель
      </router-link>
    </v-toolbar-title>

    <!-- Разделитель пространства между заголовком и кнопками справа -->
    <v-spacer />

    <!-- Блок авторизации -->
    <template v-if="authStore.isAuthenticated">
      <v-menu>
        <template #activator="{ props }">
          <v-btn v-bind="props" text class="text-none">
            <v-avatar size="32" class="me-2">
              <v-img :src="cacheBustUrl(authStore.user?.photo) || defaultPhoto" />
            </v-avatar>
            {{ userFullName }}
            <v-icon end>mdi-menu-down</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="logout">
            <v-list-item-title>Выйти</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>

    <template v-else>
      <v-btn text :to="{ name: 'login' }">Войти</v-btn>
    </template>
  </v-app-bar>

  <!-- Основной контент страницы -->
  <v-main app>
    <div class="pa-4">
      <!-- Слот для контента, передаваемого в layout -->
      <slot />
    </div>
  </v-main>
</template>

<script setup>
// Импорт реактивных инструментов Vue
import { ref, watch, computed } from 'vue'

// Импорт Vuetify утилит: определение устройства и темы
import { useDisplay } from 'vuetify'

// Импорт логотипа для отображения на странице входа
import admin from '@/assets/img/admin.jpeg'

import { cacheBustUrl } from "@/common/helpers/cacheBust";

// Импорт стора авторизации
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()

// Импорт роутера
import { useRouter } from 'vue-router'
const router = useRouter()

import defaultPhoto from '@/assets/img/user-default.png'

const userFullName = computed(() => {
  const user = authStore.user;
  return user ? `${user.first_name} ${user.last_name}` : "Нет данных";
});

const { mobile } = useDisplay();
const drawer = ref(false);

if (!mobile.value) {
  drawer.value = localStorage.getItem('drawerOpen') === 'true';
}

watch(drawer, (val) => {
  if (!mobile.value) {
    localStorage.setItem('drawerOpen', val);
  }
});

function handleMenuItemClick() {
  if (mobile.value) drawer.value = false;
}

// Элементы бокового меню
const menuItems = [
  { title: 'Проекты', icon: 'mdi-account-multiple', to: 'projects' },
  { title: 'Опыт работы', icon: 'mdi-account-multiple', to: 'experiences' },
]

// Выход пользователя и переход на страницу логина
async function logout() {
  await authStore.logout()
  router.push({ name: 'login' }) // редирект на login после logout
}
</script>

<style>
/* Стилизация основной области приложения */
</style>