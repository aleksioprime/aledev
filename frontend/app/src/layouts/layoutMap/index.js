import { defineAsyncComponent } from 'vue';
import LandingLayout from './landing/LandingLayout.vue';

// Макеты админки загружаются лениво вместе с Vuetify
export default {
  landing: LandingLayout,
  default: defineAsyncComponent(() => import('./default/DefaultLayout.vue')),
  manage: defineAsyncComponent(() => import('./manage/ManageLayout.vue')),
  // добавьте другие макеты по мере необходимости
};
