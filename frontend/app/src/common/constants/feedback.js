// Справочники формы обратной связи. Ключи совпадают с бэкендом
// (services/portfolio/app/src/constants/base.py: FEEDBACK_SERVICES / FEEDBACK_BUDGETS)
export const FEEDBACK_SERVICES = ['web', 'backend', 'iot', 'ml', 'automation', 'mentoring', 'other']
export const FEEDBACK_BUDGETS = ['lt100', '100_300', '300_700', 'gt700', 'discuss']

// Подписи для админки
export const SERVICE_LABELS = {
  web: 'Веб-сервис / сайт',
  backend: 'Backend / API',
  iot: 'IoT / устройства',
  ml: 'ML / компьютерное зрение',
  automation: 'Автоматизация',
  mentoring: 'Обучение / менторство',
  other: 'Другое',
}

export const BUDGET_LABELS = {
  lt100: 'до 100 тыс. ₽',
  '100_300': '100–300 тыс. ₽',
  '300_700': '300–700 тыс. ₽',
  gt700: 'от 700 тыс. ₽',
  discuss: 'Обсудим',
}

export const STATUS_OPTIONS = [
  { value: 'new', title: 'Новое', color: 'primary' },
  { value: 'in_progress', title: 'В работе', color: 'orange' },
  { value: 'done', title: 'Завершено', color: 'green' },
  { value: 'archived', title: 'Архив', color: 'grey' },
  { value: 'spam', title: 'Спам', color: 'red' },
]

export const EMAIL_STATUS = {
  pending: { title: 'В очереди', color: 'grey', icon: 'mdi-clock-outline' },
  sending: { title: 'Отправляется', color: 'blue', icon: 'mdi-send-clock' },
  sent: { title: 'Отправлено', color: 'green', icon: 'mdi-email-check-outline' },
  failed: { title: 'Ошибка', color: 'red', icon: 'mdi-email-alert-outline' },
}
