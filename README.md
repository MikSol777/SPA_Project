# SPA LMS Backend

Простое Django/DRF API для LMS с курсами, уроками и кастомным пользователем на email.

## Быстрый старт
- Установить зависимости: `poetry install`
- Создать `.env` на основе `env.example`
- Применить миграции: `poetry run python manage.py migrate`
- Запустить сервер: `poetry run python manage.py runserver`
- (Опционально) наполнить демо-данными: `poetry run python manage.py seed_payments`
- Создать группу модераторов: `poetry run python manage.py seed_groups`

## Основные эндпоинты
- `POST /admin/` — стандартная админка (создайте суперпользователя `poetry run python manage.py createsuperuser`)
- `POST /admin/` — стандартная админка (создайте суперпользователя `poetry run python manage.py createsuperuser`)
- `GET|POST /api/courses/` и `GET|PATCH|DELETE /api/courses/<id>/` — CRUD курсов (ViewSet, возвращает `lessons_count` и вложенные `lessons`)
- `GET|POST /api/lessons/` и `GET|PATCH|DELETE /api/lessons/<id>/` — CRUD уроков (generics)
- `GET /api/payments/` — список платежей с фильтрами (`paid_course`, `paid_lesson`, `payment_method`) и сортировкой по `payment_date` через `?ordering=payment_date` или `?ordering=-payment_date`.
- Пользователи:
  - Регистрация: `POST /api/auth/register/` (доступно без авторизации)
  - JWT: `POST /api/auth/token/`, `POST /api/auth/token/refresh/`
  - Профиль: `GET|PATCH /api/users/<id>/`
  - CRUD: `/api/users/` (список — только админ; карточка — владелец или админ)

Все эндпоинты (кроме регистрации и JWT) требуют авторизации (Bearer JWT). Модераторы могут читать/редактировать любые курсы и уроки, но не могут их создавать и удалять. Обычные пользователи работают только со своими курсами/уроками.

Используйте Postman/HTTPie с JWT-токеном: `Authorization: Bearer <access_token>`.



