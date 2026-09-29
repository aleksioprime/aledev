from enum import Enum


class LangEnum(Enum):
    """
    Языки контента
    """
    ru = "ru"
    en = "en"

class FeedbackKind(str, Enum):
    """ Тип обращения """
    order = "order"          # заказ / проект
    training = "training"    # обучение / менторство
    question = "question"    # вопрос / консультация


class FeedbackStatus(str, Enum):
    """ Статус обработки обращения в админке """
    new = "new"
    in_progress = "in_progress"
    done = "done"
    archived = "archived"
    spam = "spam"


class EmailStatus(str, Enum):
    """ Статус доставки уведомления на почту """
    pending = "pending"
    sending = "sending"
    sent = "sent"
    failed = "failed"


# Допустимые значения для полей заказа и их подписи для письма/админки
FEEDBACK_SERVICES = {
    "web": "Веб-сервис / сайт",
    "backend": "Backend / API / микросервисы",
    "iot": "IoT / устройства",
    "ml": "ML / компьютерное зрение",
    "automation": "Автоматизация / интеграции",
    "other": "Другое",
}

# Форматы обучения (для обращений типа training хранятся в поле service)
FEEDBACK_TRAINING_FORMATS = {
    "individual": "Индивидуальные занятия",
    "group": "Группа или класс",
    "team": "Менторство проектной команды",
    "corporate": "Обучение сотрудников",
    "curriculum": "Разработка курса или программы",
}

FEEDBACK_BUDGETS = {
    "lt100": "до 100 тыс. ₽",
    "100_300": "100–300 тыс. ₽",
    "300_700": "300–700 тыс. ₽",
    "gt700": "от 700 тыс. ₽",
    "discuss": "Обсудим",
}
