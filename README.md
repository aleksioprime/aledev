# Домашний проект

## Запуск для разработчика

Скачайте репозиторий:
```
git clone https://github.com/aleksioprime/aledev.git
cd hyperspectrus
```

Запустите сервис локально:
```
docker-compose -p aledev up -d --build
```

### Установка окружения

Установить [Pyenv](https://github.com/pyenv/pyenv#installation) (утилиту для управления версиями Python)
Загрузить интерпретатор Python 3.12.0:
```
pyenv install 3.12.0
```
Создать виртуальную среду:
```
pyenv virtualenv 3.12.0 lisema-venv
```
Запустить виртуальную среду:
```
pyenv activate lisema-venv
```
Установить библиотеки:
```
pip install -r requirements.txt
```

## Запуск приложения
```
docker-compose -p lisema up -d --build
```

## Создание миграций
```
docker-compose -p lisema exec auth alembic revision --autogenerate -m "Initial migration"
```