import { domainCheck } from "./domainCheck";

export const middlewarePipeline = (router) => {
  router.beforeEach(async (to, from) => {
    // Сначала проверяем домен для всех маршрутов
    await new Promise((resolve, reject) => {
      domainCheck(to, from, (result) => {
        if (result && typeof result === 'object') {
          // Если есть редирект, применяем его
          router.push(result);
          resolve();
        } else {
          resolve();
        }
      });
    });

    // Затем обрабатываем остальные middlewares
    const middlewares = to.meta.middlewares;
    if (!middlewares) {
      return true;
    }
    for (const middleware of middlewares) {
      const result = await middleware({ to, from, router });
      if (
        typeof result === "object" ||
        typeof result === "string" ||
        result === false
      ) {
        return result;
      }
    }
    return true;
  });
};