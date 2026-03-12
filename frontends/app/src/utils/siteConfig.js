const MAIN_TITLE = "Aleksei Semochkin — Software Engineer Portfolio";
const BLOG_TITLE = "AleBlog — Блог Алексея Семочкина";

export function getBaseTitleByRoute(route) {
  if (route?.name?.toString().startsWith("blog-")) {
    return BLOG_TITLE;
  }

  return MAIN_TITLE;
}
