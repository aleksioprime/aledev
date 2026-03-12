export const mainRoutes = [
  {
    path: "/admin",
    name: "login",
    component: () => import("@/views/admin/Login.vue"),
    meta: {
      title: "Администраторская панель",
    },
  },
];
