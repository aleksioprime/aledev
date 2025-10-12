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
    path: "/post/:slug",
    name: "blog-post",
    component: () => import("@/views/blog/BlogPost.vue"),
    meta: {
      title: 'Пост',
      domain: 'aleblog'
    },
  },
];