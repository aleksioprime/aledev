/**
 * Утилиты для работы с доменами в многодоменном приложении
 */

// Определяем доступные домены
export const DOMAINS = {
  ALEDEV: 'aledev.ru',
  ALEBLOG: 'aleblog.ru'
}

/**
 * Получает текущий домен
 * @returns {string} - текущий домен
 */
export function getCurrentDomain() {
  if (typeof window === 'undefined') {
    return DOMAINS.ALEDEV; // fallback для SSR
  }

  const hostname = window.location.hostname;

  // Для разработки также учитываем localhost
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    // Можно определить по порту или query параметру
    const urlParams = new URLSearchParams(window.location.search);
    const domain = urlParams.get('domain');

    if (domain === 'blog') {
      return DOMAINS.ALEBLOG;
    }

    return DOMAINS.ALEDEV; // по умолчанию
  }

  // Для продакшена проверяем точный домен
  if (hostname.includes('aleblog.ru')) {
    return DOMAINS.ALEBLOG;
  }

  return DOMAINS.ALEDEV; // по умолчанию
}

/**
 * Проверяет, является ли текущий домен блогом
 * @returns {boolean}
 */
export function isBlogDomain() {
  return getCurrentDomain() === DOMAINS.ALEBLOG;
}

/**
 * Проверяет, является ли текущий домен основным сайтом
 * @returns {boolean}
 */
export function isMainDomain() {
  return getCurrentDomain() === DOMAINS.ALEDEV;
}

/**
 * Получает конфигурацию для текущего домена
 * @returns {Object} - конфигурация домена
 */
export function getDomainConfig() {
  const domain = getCurrentDomain();

  const configs = {
    [DOMAINS.ALEDEV]: {
      title: 'Aleksei Semochkin — Software Engineer Portfolio',
      defaultLayout: 'default',
      routes: 'aledev'
    },
    [DOMAINS.ALEBLOG]: {
      title: 'AleBlog — Блог Алексея Семочкина',
      defaultLayout: 'blog',
      routes: 'aleblog'
    }
  };

  return configs[domain] || configs[DOMAINS.ALEDEV];
}