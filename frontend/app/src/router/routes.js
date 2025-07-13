import { isLoggedIn } from "@/middlewares/isLoggedIn";

export const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/HomeView.vue"),
    meta: {
      title: '',
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import("@/views/NotFound.vue"),
    meta: {
      title: 'Страница не найдена',
    },
  },
]