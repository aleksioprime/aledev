"""portfolio content: projects, experience, prize metric

Revision ID: 7b2e4c9a1d35
Revises: 10865b216202
Create Date: 2026-09-29 13:30:00.000000

"""
from datetime import date, datetime, timezone
from typing import Sequence, Union
from uuid import UUID

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '7b2e4c9a1d35'
down_revision: Union[str, None] = '10865b216202'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Записи создаются с фиксированными id: миграция заменяет только их,
# проекты и опыт, добавленные через админку, не трогаются.
PROJECTS = [
    {
        'stack': 'Django, DRF, Vue 3, Pinia, PostgreSQL, Celery, Redis, OpenRouter, Docker, Kubernetes',
        'ru': (
            'SkolStream — платформа администрирования учебного процесса',
            'Веб-платформа Международной гимназии «Сколково» для учебного процесса по стандартам '
            'Международного бакалавриата: юниты, итоговые работы, репорты, портфолио, проекты и конкурсы.',
            'Модульный монолит на Django REST Framework и SPA на Vue 3 (Composition API, Pinia). '
            'Автоматизирует ключевые процессы школы по стандартам IB: создание учебных юнитов, график '
            'итоговых работ, индивидуальные репорты учеников, модерацию проектов и конкурсов, портфолио '
            'с подтверждением записей учителем.\n\n'
            'JWT-аутентификация и ролевая модель доступа: права и видимость данных проверяются на сервере. '
            'Всё долгое вынесено в Celery — синхронизация оценок с «Дневник.ру» (идемпотентная, с повторами '
            'при сбоях), экспорт документов, рассылки и плановые напоминания без дублей. Экспериментальный '
            'AI-сервис готовит черновики репортов и анализирует достижения. Тесты на pytest, развёртывание '
            'в Docker и Kubernetes. Провёл юзабилити-тестирование, внедрение и сопровождаю проект.',
        ),
        'en': (
            'SkolStream — academic administration platform',
            'A web platform for the Skolkovo International Gymnasium that runs the IB learning process: '
            'units, summative assessments, reports, portfolios, projects and competitions.',
            'A modular monolith on Django REST Framework with a Vue 3 SPA (Composition API, Pinia). It '
            'automates the school\'s key IB processes: building learning units, scheduling summative '
            'assessments, individual student reports, moderation of projects and competitions, and '
            'portfolios with teacher approval.\n\n'
            'JWT authentication and role-based access with permissions and data scoping enforced on the '
            'server. Long-running work runs in Celery: grade sync with Dnevnik.ru (idempotent, retried on '
            'failures), document export, mailings and scheduled reminders without duplicates. An '
            'experimental AI service drafts reports and analyses achievements. Tested with pytest, deployed '
            'with Docker and Kubernetes. I ran usability testing and rollout and keep supporting the project.',
        ),
    },
    {
        'stack': 'FastAPI, SQLAlchemy, PostgreSQL, RabbitMQ, Redis, APScheduler, aiogram, Moodle, Vue 3, Docker',
        'ru': (
            'Платформа сопровождения слушателей ДПО',
            'Микросервисная платформа для программ дополнительного профессионального образования: '
            'приём заявок, обучение, рефлексивная практика и уведомления во всех каналах.',
            'Набор независимых сервисов на асинхронном Python: REST API на FastAPI, планировщик на '
            'APScheduler (воронка заявок и напоминания), сервис уведомлений — email, Telegram, мессенджер '
            'Max и in-app, боты на aiogram и синхронизация слушателей с Moodle.\n\n'
            'Сервисы не вызывают друг друга напрямую: данные — в PostgreSQL, события — в RabbitMQ '
            '(durable-очереди, повторы, dead-letter), поэтому сбой одного сервиса не останавливает остальные. '
            'Redis — для кэша, лимитов запросов и отзыва токенов; JWT с ротацией refresh-токенов и '
            'обнаружением их повторного использования. Слоистая архитектура с Unit of Work, фронтенд на '
            'Vue 3 и Vuetify, CI/CD на GitHub Actions.',
        ),
        'en': (
            'Continuing education learner platform',
            'A microservice platform for continuing professional education programmes: admissions, '
            'learning, reflective practice and notifications across every channel.',
            'Independent services on async Python: a FastAPI REST API, an APScheduler scheduler (admissions '
            'funnel and reminders), a notification service for email, Telegram, the Max messenger and '
            'in-app, aiogram bots and learner sync with Moodle.\n\n'
            'Services never call each other directly: data lives in PostgreSQL and events go through '
            'RabbitMQ (durable queues, retries, dead-lettering), so one failing service does not stop the '
            'rest. Redis handles caching, rate limits and token revocation; JWT with refresh-token rotation '
            'and reuse detection. Layered architecture with Unit of Work, Vue 3 and Vuetify frontend, CI/CD '
            'on GitHub Actions.',
        ),
    },
    {
        'stack': 'Python, FastAPI, PostgreSQL, Celery, NumPy, OpenCV, Vue 3, Vuetify, PyQt, Raspberry Pi, Arduino',
        'ru': (
            'Hyperspectrus — комплекс гиперспектральной диагностики',
            'Программный комплекс медицинского стартапа: устройство многоспектральной съёмки на '
            'Raspberry Pi, рабочее место врача и веб-платформа для клиник.',
            'Устройство снимает серию кадров кожи под подсветкой семи длин волн (520–940 нм): приложение '
            'на PyQt в киоск-режиме, управление светодиодами через GPIO или Arduino и локальный REST API '
            'для постановки задач съёмки.\n\n'
            'Оконное приложение врача работает автономно: пациенты, сеансы, загрузка снимков с устройства '
            'и обработка без интернета. Веб-платформа ведёт пациентов нескольких клиник, управляет сеансами '
            'и параметрами устройств, а обработку выполняет асинхронно в Celery: по закону '
            'Бугера—Ламберта—Бера и методу наименьших квадратов строит карты распределения хромофоров, '
            'выделяет очаг и формирует аналитический отчёт по каждому исследованию.',
        ),
        'en': (
            'Hyperspectrus — hyperspectral diagnostics suite',
            'Software for a medical startup: a multispectral imaging device on Raspberry Pi, a '
            'doctor\'s workstation and a web platform for clinics.',
            'The device captures a series of skin images under seven wavelengths (520–940 nm): a kiosk '
            'PyQt app, LED control via GPIO or Arduino, and a local REST API for imaging tasks.\n\n'
            'The doctor\'s desktop app works offline: patients, sessions, image download from the device '
            'and local processing. The web platform manages patients of several clinics, sessions and '
            'device settings, and processes studies asynchronously in Celery: using the Beer–Lambert law '
            'and least squares it builds chromophore distribution maps, segments the lesion and produces '
            'an analytical report for every study.',
        ),
    },
    {
        'stack': 'Python, FastAPI, PostgreSQL, MQTT, Mosquitto, Vue.js, Vuetify, Arduino',
        'ru': (
            'ЕмПолимер — мониторинг биоустановок',
            'Дашборд для наблюдения в реальном времени за микроклиматом установок биодеградации полиэтилена.',
            'Каждая установка оснащена модулем на Arduino, который передаёт показания датчиков по GPRS на '
            'MQTT-брокер Mosquitto. Асинхронный воркер подписан на топики, принимает сообщения и сохраняет '
            'данные в PostgreSQL. В веб-интерфейсе можно добавлять и настраивать карточки установок, '
            'смотреть текущие и исторические параметры микроклимата.',
        ),
        'en': (
            'EmPolymer — biofacility monitoring',
            'A real-time dashboard for the microclimate of polyethylene biodegradation units.',
            'Each unit has an Arduino module that sends sensor readings over GPRS to a Mosquitto MQTT '
            'broker. An async worker subscribes to the topics and stores the data in PostgreSQL. In the web '
            'interface users add and configure unit cards and view current and historical microclimate '
            'parameters.',
        ),
    },
    {
        'stack': 'Python, OpenCV, Neural networks, Raspberry Pi, 3D',
        'ru': (
            'Образовательная платформа для изучения технического зрения',
            'Грантовый проект: мобильная платформа с нейросетями для распознавания дорожных знаков, '
            'испытательный полигон и учебные материалы для школьников.',
            'Исследовал алгоритмы машинного обучения на наборах изображений дорожных знаков: поиск объекта '
            'по всему кадру видеопотока, локализацию и распознавание фрагмента разными архитектурами '
            'нейросетей. Собрал экспериментальную мобильную платформу на шасси с рулевым управлением '
            'Аккермана, элементы испытательного полигона и 3D-визуализацию для планирования дорожных '
            'ситуаций. Разработки легли в основу занятий по компьютерному зрению со стереокамерами и '
            'учебного кейса, победившего во всероссийском конкурсе.',
        ),
        'en': (
            'Educational platform for learning machine vision',
            'A grant project: a mobile platform with neural networks for traffic sign recognition, a test '
            'track and teaching materials for school students.',
            'I studied machine learning approaches on traffic sign image sets: detecting objects across the '
            'whole video frame, localising them and classifying the crop with different neural network '
            'architectures. I built an experimental mobile platform on an Ackermann-steering chassis, test '
            'track elements and a 3D visualisation for planning road scenarios. The work became the basis '
            'of lessons on computer vision with stereo cameras and of a teaching case that won a national '
            'contest.',
        ),
    },
]

EXPERIENCE = [
    {
        'start': date(2023, 9, 1), 'end': None, 'current': True,
        'ru': (
            'Инженер-программист, тьютор', 'Международная гимназия «Сколково»',
            'Веб-разработка на FastAPI и Django, проектирование и внедрение сервисов для администрирования '
            'учебного процесса',
            'Разработал и внедрил комплекс модулей веб-приложения, автоматизирующего ключевые образовательные '
            'и административные процессы школы по стандартам Международного бакалавриата: учебные юниты, '
            'индивидуальные репорты учеников, график итоговых работ, модерация проектов и конкурсов, '
            'портфолио. Реализовал экспериментальный AI-сервис для анализа достижений. Провёл '
            'юзабилити-тестирование, внедрение и сопровождение проекта. Организовал менторство в детских '
            'IT-проектах и конкурсах.',
        ),
        'en': (
            'Software Engineer, Tutor', 'Skolkovo International Gymnasium',
            'Web development with FastAPI and Django, designing and delivering services for academic '
            'administration',
            'Built and rolled out a suite of web application modules that automate the school\'s key '
            'educational and administrative processes to International Baccalaureate standards: learning '
            'units, individual student reports, summative assessment scheduling, project and competition '
            'moderation, and portfolios. Implemented an experimental AI service for achievement analysis. '
            'Ran usability testing, rollout and ongoing support. Organised mentoring for children\'s IT '
            'projects and competitions.',
        ),
    },
    {
        'start': date(2019, 6, 1), 'end': None, 'current': True,
        'ru': (
            'Разработчик и ментор IT-проектов', 'Фриланс, проекты со стартапами',
            'Разработка web-приложений, IoT- и ML-сервисов',
            'Разрабатываю микросервисную платформу сопровождения слушателей программ дополнительного '
            'профессионального образования. Для стартапа Hyperspectrus создал комплексное ПО: приложение '
            'устройства гиперспектральной съёмки на Raspberry Pi, оконное приложение для сбора и анализа '
            'снимков и веб-приложение для централизованного учёта и исследования результатов. Для стартапа '
            '«ЕмПолимер» разработал ПО мониторинга микроклимата в установке биодеградации полиэтилена — для '
            'управляющего устройства и сервера. Выиграл грант на разработку образовательной платформы для '
            'изучения технического зрения: реализовал алгоритмы машинного зрения и апробировал их в учебных '
            'задачах.',
        ),
        'en': (
            'Developer and Mentor of IT Projects', 'Freelance, startup projects',
            'Development of web applications, IoT and ML services',
            'Building a microservice platform that supports learners of continuing professional education '
            'programmes. For the Hyperspectrus startup I built the full software suite: the app for a '
            'Raspberry Pi hyperspectral imaging device, a desktop app for capturing and analysing images, '
            'and a web application for centralised records and research. For the EmPolymer startup I built '
            'microclimate monitoring software for a polyethylene biodegradation unit, covering both the '
            'control device and the server. Won a grant to develop an educational platform for learning '
            'machine vision: implemented machine vision algorithms and tested them in teaching tasks.',
        ),
    },
    {
        'start': date(2016, 7, 19), 'end': date(2024, 8, 31), 'current': False,
        'ru': (
            'Заведующий кафедрой, учитель технических дисциплин', 'Международная гимназия «Сколково»',
            'Разработка образовательных программ и курсов IT-направления, менторство',
            'Разработал и внедрил учебные программы для средней и старшей школы: технологии с элементами '
            'робототехники, основы Python, 3D-моделирование, программируемая электроника, компьютерная '
            'графика и основы машинного обучения. Вёл курсы Python как преподаватель Яндекс Лицея и курсы '
            'по ИИ как коуч Intel AI for Youth. Победитель конкурса учебных кейсов: цикл уроков по '
            'распознаванию дорожных знаков с помощью Python и ИИ; руководил проектом-призёром по анализу '
            'социальных контактов. Был IT-ментором для коллег, помогал им в профессиональных задачах.',
        ),
        'en': (
            'Head of Department, Teacher of Technical Subjects', 'Skolkovo International Gymnasium',
            'Development of IT curricula and courses, mentoring',
            'Designed and delivered middle and high school curricula: technology with robotics, Python '
            'basics, 3D modelling, programmable electronics, computer graphics and machine learning '
            'fundamentals. Taught Python as a Yandex Lyceum instructor and AI as an Intel AI for Youth coach. '
            'Winner of a teaching case contest with a lesson series on traffic sign recognition using Python '
            'and AI; supervised an award-winning project on social contact analysis. Mentored colleagues in '
            'IT and supported their professional growth.',
        ),
    },
    {
        'start': date(2014, 9, 1), 'end': date(2016, 7, 31), 'current': False,
        'ru': (
            'Методист, преподаватель робототехники', 'Центр развития творчества детей и юношества, Пенза',
            'Разработка образовательных курсов и конкурсных задач, организация соревнований',
            'Организовывал ежегодные отборочные соревнования по робототехнике вместе с оргкомитетами '
            '«Робофеста» и World Robot Olympiad. Вёл курсы для учителей и учеников региона, разработал '
            'эталонные решения конкурсных задач на Robolab и RobotC для Lego Mindstorms, C++ для Arduino и '
            'Python для Raspberry Pi. Подготовил школьников Пензенской области, занявших призовые места на '
            'межрегиональных и всероссийских робототехнических конкурсах.',
        ),
        'en': (
            'Methodologist, Robotics Instructor', 'Center for Children\'s and Youth Creativity, Penza',
            'Development of courses and competition tasks, organisation of competitions',
            'Organised annual robotics qualifiers together with the Robofest and World Robot Olympiad '
            'committees. Ran courses for teachers and students of the region and built reference solutions '
            'for competition tasks in Robolab and RobotC for Lego Mindstorms, C++ for Arduino and Python for '
            'Raspberry Pi. Prepared Penza region students who won prizes at interregional and national '
            'robotics competitions.',
        ),
    },
]


def _project_id(index: int) -> UUID:
    return UUID(f'40000000-0000-4000-8000-{index + 1:012d}')


def _project_translation_id(index: int, lang_index: int) -> UUID:
    return UUID(f'41000000-0000-4000-8000-{index + 1:010d}{lang_index:02d}')


def _experience_id(index: int) -> UUID:
    return UUID(f'50000000-0000-4000-8000-{index + 1:012d}')


def _experience_translation_id(index: int, lang_index: int) -> UUID:
    return UUID(f'51000000-0000-4000-8000-{index + 1:010d}{lang_index:02d}')


def _delete_seeded(conn) -> None:
    project_ids = [_project_id(i) for i in range(len(PROJECTS))]
    experience_ids = [_experience_id(i) for i in range(len(EXPERIENCE))]
    conn.execute(sa.text('DELETE FROM project_translations WHERE project_id = ANY(:ids)'), {'ids': project_ids})
    conn.execute(sa.text('DELETE FROM articles WHERE project_id = ANY(:ids)'), {'ids': project_ids})
    conn.execute(sa.text('DELETE FROM projects WHERE id = ANY(:ids)'), {'ids': project_ids})
    conn.execute(sa.text('DELETE FROM experience_translations WHERE experience_id = ANY(:ids)'), {'ids': experience_ids})
    conn.execute(sa.text('DELETE FROM experiences WHERE id = ANY(:ids)'), {'ids': experience_ids})


def upgrade() -> None:
    conn = op.get_bind()
    lang_enum = postgresql.ENUM('ru', 'en', name='langenum', create_type=False)
    now = datetime(2026, 9, 29, tzinfo=timezone.utc)

    _delete_seeded(conn)

    # Свои проекты — первыми, проекты из админки сдвигаются следом
    conn.execute(sa.text('UPDATE projects SET "order" = "order" + :n'), {'n': len(PROJECTS)})

    project_table = sa.table(
        'projects', sa.column('id', sa.Uuid()), sa.column('order', sa.Integer()),
        sa.column('stack', sa.String()), sa.column('link', sa.String()),
        sa.column('github_url', sa.String()), sa.column('demo_url', sa.String()),
        sa.column('is_favorite', sa.Boolean()), sa.column('created_at', sa.DateTime(timezone=True)),
        sa.column('updated_at', sa.DateTime(timezone=True)),
    )
    project_translation_table = sa.table(
        'project_translations', sa.column('id', sa.Uuid()), sa.column('project_id', sa.Uuid()),
        sa.column('lang', lang_enum), sa.column('title', sa.String()),
        sa.column('short_description', sa.String()), sa.column('description', sa.Text()),
    )
    op.bulk_insert(project_table, [
        {
            'id': _project_id(i), 'order': i, 'stack': p['stack'], 'link': None, 'github_url': None,
            'demo_url': None, 'is_favorite': True, 'created_at': now, 'updated_at': now,
        }
        for i, p in enumerate(PROJECTS)
    ])
    op.bulk_insert(project_translation_table, [
        {
            'id': _project_translation_id(i, li), 'project_id': _project_id(i), 'lang': lang,
            'title': p[lang][0], 'short_description': p[lang][1], 'description': p[lang][2],
        }
        for i, p in enumerate(PROJECTS)
        for li, lang in enumerate(('ru', 'en'), start=1)
    ])

    experience_table = sa.table(
        'experiences', sa.column('id', sa.Uuid()), sa.column('start_date', sa.Date()),
        sa.column('end_date', sa.Date()), sa.column('is_current', sa.Boolean()),
        sa.column('created_at', sa.DateTime(timezone=True)),
    )
    experience_translation_table = sa.table(
        'experience_translations', sa.column('id', sa.Uuid()), sa.column('experience_id', sa.Uuid()),
        sa.column('lang', lang_enum), sa.column('position', sa.String()), sa.column('company', sa.String()),
        sa.column('responsibilities', sa.Text()), sa.column('description', sa.Text()),
    )
    op.bulk_insert(experience_table, [
        {
            'id': _experience_id(i), 'start_date': e['start'], 'end_date': e['end'],
            'is_current': e['current'], 'created_at': now,
        }
        for i, e in enumerate(EXPERIENCE)
    ])
    op.bulk_insert(experience_translation_table, [
        {
            'id': _experience_translation_id(i, li), 'experience_id': _experience_id(i), 'lang': lang,
            'position': e[lang][0], 'company': e[lang][1],
            'responsibilities': e[lang][2], 'description': e[lang][3],
        }
        for i, e in enumerate(EXPERIENCE)
        for li, lang in enumerate(('ru', 'en'), start=1)
    ])

    conn.execute(sa.text("UPDATE mentoring_metrics SET value = '20+' WHERE key = 'prizes'"))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("UPDATE mentoring_metrics SET value = '20' WHERE key = 'prizes'"))
    _delete_seeded(conn)
    conn.execute(sa.text('UPDATE projects SET "order" = GREATEST("order" - :n, 0)'), {'n': len(PROJECTS)})
