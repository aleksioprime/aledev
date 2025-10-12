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

export const routes = getRoutesForDomain();