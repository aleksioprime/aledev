import { mainRoutes } from "./mainRoutes";

export const routes = [
  ...mainRoutes,
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("@/views/NotFound.vue"),
    meta: {
      title: "Страница не найдена",
    },
  },
];
