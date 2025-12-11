# SPA LMS Backend

Простое Django/DRF API для LMS с курсами, уроками и кастомным пользователем на email.

## Быстрый старт
- Установить зависимости: `poetry install`
- Создать `.env` на основе `env.example`
- Применить миграции: `poetry run python manage.py migrate`
- Запустить сервер: `poetry run python manage.py runserver`
- (Опционально) наполнить демо-данными: `poetry run python manage.py seed_payments`

## Основные эндпоинты
- `POST /admin/` — стандартная админка (создайте суперпользователя `poetry run python manage.py createsuperuser`)
- `GET|POST /api/courses/` и `GET|PATCH|DELETE /api/courses/<id>/` — CRUD курсов (ViewSet, возвращает `lessons_count` и вложенные `lessons`)
- `GET|POST /api/lessons/` и `GET|PATCH|DELETE /api/lessons/<id>/` — CRUD уроков (generics)
- `GET /api/payments/` — список платежей с фильтрами (`paid_course`, `paid_lesson`, `payment_method`) и сортировкой по `payment_date` через `?ordering=payment_date` или `?ordering=-payment_date`.
- `GET|PATCH /api/users/<id>/` — просмотр/редактирование профиля пользователя (email read-only).

Аутентификация пока не подключена — для тестов используйте Postman без токенов.



