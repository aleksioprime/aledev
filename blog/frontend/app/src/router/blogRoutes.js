import { isLoggedIn } from "@/middlewares/isLoggedIn";

export const blogRoutes = [
  {
    path: "/",
    name: "blog-home",
    component: () => import("@/views/blog/BlogHome.vue"),
    meta: {
      title: "",
    },
  },
  {
    path: "/posts",
    name: "blog-posts",
    component: () => import("@/views/blog/BlogPosts.vue"),
    meta: {
      title: "Все посты",
    },
  },
  {
    path: "/posts/create",
    name: "blog-post-create",
    component: () => import("@/views/blog/BlogPostCreate.vue"),
    meta: {
      title: "Создать пост",
      middlewares: [isLoggedIn],
    },
  },
  {
    path: "/posts/:id/edit",
    name: "blog-post-edit",
    component: () => import("@/views/blog/BlogPostEdit.vue"),
    meta: {
      title: "Редактировать пост",
      middlewares: [isLoggedIn],
    },
  },
  {
    path: "/post/:slug",
    name: "blog-post",
    component: () => import("@/views/blog/BlogPost.vue"),
    meta: {
      title: "Пост",
    },
  },
];
