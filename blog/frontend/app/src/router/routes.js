import { mainRoutes } from "./mainRoutes";
import { blogRoutes } from "./blogRoutes";

export const routes = [
  ...mainRoutes,
  ...blogRoutes,
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("@/views/NotFound.vue"),
    meta: {
      title: "Страница не найдена",
    },
  },
];
