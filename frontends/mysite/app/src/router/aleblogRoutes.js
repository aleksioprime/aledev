import { isLoggedIn } from "@/middlewares/isLoggedIn";

// Маршруты для aleblog.ru (блог)
export const aleblogRoutes = [
  {
    path: "/",
    name: "blog-home",
    component: () => import("@/views/blog/BlogHome.vue"),
    meta: {
      title: '',
      domain: 'aleblog'
    },
  },
  {
    path: "/posts",
    name: "blog-posts",
    component: () => import("@/views/blog/BlogPosts.vue"),
    meta: {
      title: 'Все посты',
      domain: 'aleblog'
    },
  },
  {
    path: "/posts/create",
    name: "blog-post-create",
    component: () => import("@/views/blog/BlogPostCreate.vue"),
    meta: {
      title: 'Создать пост',
      domain: 'aleblog',
      middlewares: [isLoggedIn],
    },
  },
  {
    path: "/posts/:id/edit",
    name: "blog-post-edit",
    component: () => import("@/views/blog/BlogPostEdit.vue"),
    meta: {
      title: 'Редактировать пост',
      domain: 'aleblog',
      middlewares: [isLoggedIn],
    },
  },
  {
    path: "/post/:slug",
    name: "blog-post",
    component: () => import("@/views/blog/BlogPost.vue"),
    meta: {
      title: 'Пост',
      domain: 'aleblog'
    },
  },
];