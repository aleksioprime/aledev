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
  let correctHomeRoute = '';

  switch (currentDomain) {
    case DOMAINS.ALEBLOG:
      availableRoutes = aleblogRoutes;
      expectedDomainShort = 'aleblog';
      correctHomeRoute = 'blog-home';
      console.log(`Using ALEBLOG routes (${availableRoutes.length} routes)`);
      break;
    case DOMAINS.ALEDEV:
    default:
      availableRoutes = aledevRoutes;
      expectedDomainShort = 'aledev';
      correctHomeRoute = 'home';
      console.log(`Using ALEDEV routes (${availableRoutes.length} routes)`);
      break;
  }

  // Специальная обработка для главной страницы "/"
  if (to.path === '/' && to.name !== correctHomeRoute) {
    next({ name: correctHomeRoute });
    return;
  }

  // Проверяем meta.domain если он указан
  if (to.meta && to.meta.domain && to.meta.domain !== expectedDomainShort) {
    // Если домен маршрута не соответствует текущему, перенаправляем на главную
    next({ name: correctHomeRoute });
    return;
  }

  // Проверяем, есть ли целевой маршрут среди доступных для текущего домена
  const routeExists = availableRoutes.some(route => route.name === to.name);

  if (!routeExists) {
    // Если маршрут не найден для текущего домена, перенаправляем на главную страницу
    next({ name: correctHomeRoute });
    return;
  }

  // Все проверки пройдены, продолжаем
  next();
};