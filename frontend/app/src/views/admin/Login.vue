<template>
  <div class="auth-wrapper d-flex flex-column align-center justify-center fill-height pa-4">
    <div style="margin-bottom: 19vh; width:100%">

      <!-- Логотип и название -->
      <div class="mb-6 text-center">
        <div class="text-h5 font-weight-bold" style="letter-spacing:1px;">Личный кабинет</div>
      </div>

      <!-- Форма авторизации пользователя -->
      <v-card class="pa-4 mx-auto" max-width="400" elevation="8">

        <!-- Поля для ввода логина и пароля -->
        <v-form @submit.prevent="login" ref="formRef" validate-on="submit">
          <v-text-field v-model="form.username" label="Пользователь" type="text" prepend-inner-icon="mdi-account"
            :rules="[rules.required]" autocomplete="username" autofocus required density="comfortable"
            variant="outlined" class="mb-1" />
          <v-text-field v-model="form.password" label="Пароль" type="password" prepend-inner-icon="mdi-lock"
            :rules="[rules.required]" autocomplete="current-password" required density="comfortable" variant="outlined"
            class="mb-2" />

          <!-- Сообщение об ошибке сервера -->
          <v-alert v-if="serverErrorMessage" type="error" variant="tonal" class="mb-4" border="start">
            {{ serverErrorMessage }}
          </v-alert>

          <v-btn type="submit" color="primary" size="large" block elevation="2" :loading="loading">
            Войти
          </v-btn>
          <div class="text-center">
            <v-btn :to="{ name: 'home' }" color="secondary" variant="outlined" class="mt-10">
              <v-icon start>mdi-arrow-left</v-icon>
              Вернуться на главную
            </v-btn>
          </div>
        </v-form>

      </v-card>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import jwtService from "@/services/jwt/jwt.service";
import rules from "@/common/helpers/rules";

import { useRouter } from 'vue-router';
const router = useRouter()

import { useAuthStore } from '@/stores';
const authStore = useAuthStore()

const formRef = ref();

const serverErrorMessage = ref(null)
const loading = ref(false)

// Локальное состояние формы
const form = reactive({
  username: "",
  password: "",
});

// Авторизация пользователя
const login = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;

  loading.value = true
  const credentials = {
    username: form.username,
    password: form.password
  }
  serverErrorMessage.value = null

  const responseMessage = await authStore.login(credentials)
  loading.value = false

  if (responseMessage !== 'success') {
    serverErrorMessage.value = responseMessage;
    return
  }
  await authStore.getMe();
  await router.push({ name: "projects" });
}

onMounted(async () => {
  const accessToken = jwtService.getAccessToken();

  if (accessToken && authStore.isAuthenticated) {
    router.push({ name: "projects" });
  }
})
</script>

<style scoped>
.auth-wrapper {
  min-height: 100vh;
  min-width: 100vw;
  background: linear-gradient(120deg, #f8fafc 0%, #e0e7ef 100%);
}

@media (max-width: 600px) {
  .auth-wrapper .v-card {
    max-width: 100vw !important;
    width: 100vw !important;
    border-radius: 0 !important;
  }

  .auth-wrapper {
    padding: 0 !important;
  }
}
</style>