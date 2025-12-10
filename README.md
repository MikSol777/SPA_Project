# SPA LMS Backend

Простое Django/DRF API для LMS с курсами, уроками и кастомным пользователем на email.

## Быстрый старт
- Установить зависимости: `poetry install`
- Применить миграции (уже созданы): `poetry run python manage.py migrate`
- Запустить сервер: `poetry run python manage.py runserver`

## Основные эндпоинты
- `POST /admin/` — стандартная админка (создайте суперпользователя `poetry run python manage.py createsuperuser`)
- `GET|POST /api/courses/` и `GET|PATCH|DELETE /api/courses/<id>/` — CRUD курсов (ViewSet)
- `GET|POST /api/lessons/` и `GET|PATCH|DELETE /api/lessons/<id>/` — CRUD уроков (generics)

Аутентификация пока не подключена — для тестов используйте Postman без токенов.



