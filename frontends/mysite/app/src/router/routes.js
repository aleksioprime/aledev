import { aledevRoutes } from "./aledevRoutes";
import { aleblogRoutes } from "./aleblogRoutes";
import { getCurrentDomain, DOMAINS } from "@/utils/domainUtils";

/**
 * Получает маршруты для текущего домена
 * @returns {Array} - массив маршрутов
 */
function getRoutesForDomain() {
  const domain = getCurrentDomain();

  let domainRoutes = [];

  switch (domain) {
    case DOMAINS.ALEBLOG:
      domainRoutes = aleblogRoutes;
      break;
    case DOMAINS.ALEDEV:
    default:
      domainRoutes = aledevRoutes;
      break;
  }

  // Добавляем общий маршрут 404 для всех доменов
  const notFoundRoute = {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import("@/views/NotFound.vue"),
    meta: {
      title: 'Страница не найдена',
      domain: domain === DOMAINS.ALEBLOG ? 'aleblog' : 'aledev'
    },
  };

  return [...domainRoutes, notFoundRoute];
}

/**
 * Объединяем все маршруты всех доменов для единого роутера
 * В runtime будем фильтровать по домену
 * @returns {Array} - полный массив маршрутов
 */
function getAllRoutes() {
  // Объединяем все маршруты и добавляем общий 404
  const allRoutes = [
    ...aledevRoutes,
    ...aleblogRoutes,
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import("@/views/NotFound.vue"),
      meta: {
        title: 'Страница не найдена',
      },
    }
  ];

  return allRoutes;
}

// Экспортируем функцию для получения маршрутов для конкретного домена
export { getRoutesForDomain };

// Экспортируем все маршруты для роутера (статически)
export const routes = getAllRoutes();