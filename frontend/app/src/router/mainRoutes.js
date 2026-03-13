import { isLoggedIn } from "@/middlewares/isLoggedIn";

export const mainRoutes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/HomeView.vue"),
    meta: {
      title: "",
    },
  },
  {
    path: "/admin",
    name: "login",
    component: () => import("@/views/admin/Login.vue"),
    meta: {
      title: "Администраторская панель",
    },
  },
  {
    path: "/admin/projects",
    name: "projects",
    component: () => import("@/views/admin/ProjectView.vue"),
    meta: {
      title: "Проекты",
      layout: "manage",
      middlewares: [isLoggedIn],
    },
  },
  {
    path: "/admin/experience",
    name: "experiences",
    component: () => import("@/views/admin/ExperienceView.vue"),
    meta: {
      title: "Опыта работы",
      layout: "manage",
      middlewares: [isLoggedIn],
    },
  },
];
