// Импортируем функцию для создания приложения Vue
import { createApp } from 'vue'
// Импортируем главный компонент App.vue
import App from "@/App.vue";
// Импортируем i18n (мультиязычность)
import i18n from './i18n'

// Импорт модуля хранилища Pinia
import { createPinia } from 'pinia'

// Импорт модуля навигации Vue Router
import router from "@/router";

// Vuetify подключается лениво - только для админ-панели
import { installVuetify } from '@/plugins/vuetify'

// Импортируем директивы анимаций (v-reveal, v-magnetic, v-tilt)
import directivesPlugin from '@/directives'

// Импортируем стили приложения
import '@/assets/styles/main.css'

// Создаём Vue-приложение, передавая главный компонент App
const app = createApp(App);
// Подключаем Pinia для общего хранилища
app.use(createPinia());
// Перед переходом на страницы с Vuetify-разметкой (админка) загружаем Vuetify
router.beforeEach((to) => (to.meta.layout === 'landing' ? true : installVuetify(app).then(() => true)));
// Подключем Vue Router для навигации
app.use(router);
// Подключаем i18n для мультиязычности
app.use(i18n);
// Подключаем директивы анимаций лендинга
app.use(directivesPlugin);
// Монтируем приложение в элемент с id="app"
app.mount("#app");
