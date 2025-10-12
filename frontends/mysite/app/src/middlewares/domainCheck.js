import { getCurrentDomain, DOMAINS } from "@/utils/domainUtils";
import { aledevRoutes } from "@/router/aledevRoutes";
import { aleblogRoutes } from "@/router/aleblogRoutes";

/**
 * Middleware для проверки соответствия маршрута текущему домену
 * @param {Object} to - целевой маршрут
 * @param {Object} from - текущий маршрут
 * @param {Function} next - функция продолжения
 */
export const domainCheck = (to, from, next) => {
  // Пропускаем проверку для NotFound маршрута
  if (to.name === 'NotFound') {
    next();
    return;
  }

  const currentDomain = getCurrentDomain();

  // Получаем доступные маршруты для текущего домена
  let availableRoutes = [];
  let expectedDomainShort = '';

  switch (currentDomain) {
    case DOMAINS.ALEBLOG:
      availableRoutes = aleblogRoutes;
      expectedDomainShort = 'aleblog';
      break;
    case DOMAINS.ALEDEV:
    default:
      availableRoutes = aledevRoutes;
      expectedDomainShort = 'aledev';
      break;
  }

  // Проверяем meta.domain если он указан
  if (to.meta && to.meta.domain && to.meta.domain !== expectedDomainShort) {
    console.log(`Domain mismatch: route domain "${to.meta.domain}" != current domain "${expectedDomainShort}"`);
    // Если домен маршрута не соответствует текущему, перенаправляем на главную
    const homeRoute = availableRoutes.find(route => route.path === '/');
    if (homeRoute) {
      next({ name: homeRoute.name });
      return;
    }
  }

  // Проверяем, есть ли целевой маршрут среди доступных для текущего домена
  const routeExists = availableRoutes.some(route => route.name === to.name);

  if (!routeExists) {
    console.log(`Route "${to.name}" not found in ${expectedDomainShort} routes`);
    // Если маршрут не найден для текущего домена, перенаправляем на главную страницу
    const homeRoute = availableRoutes.find(route => route.path === '/');
    if (homeRoute) {
      next({ name: homeRoute.name });
      return;
    }
  }

  // Все проверки пройдены, продолжаем
  console.log(`Domain check passed for route "${to.name}" on domain "${expectedDomainShort}"`);
  next();
};