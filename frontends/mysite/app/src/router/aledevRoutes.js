import { isLoggedIn } from "@/middlewares/isLoggedIn";

// Маршруты для aledev.ru (основной сайт-портфолио)
export const aledevRoutes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/HomeView.vue"),
    meta: {
      title: '',
      domain: 'aledev'
    },
  },
  {
    path: "/admin",
    name: "login",
    component: () => import("@/views/admin/Login.vue"),
    meta: {
      title: 'Администраторская панель',
      domain: 'aledev'
    },
  },
  {
    path: "/admin/projects",
    name: "projects",
    component: () => import("@/views/admin/ProjectView.vue"),
    meta: {
      title: 'Проекты',
      layout: "manage",
      middlewares: [isLoggedIn],
      domain: 'aledev'
    },
  },
  {
    path: "/admin/experience",
    name: "experiences",
    component: () => import("@/views/admin/ExperienceView.vue"),
    meta: {
      title: 'Опыта работы',
      layout: "manage",
      middlewares: [isLoggedIn],
      domain: 'aledev'
    },
  },
];