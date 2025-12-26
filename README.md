# SPA LMS Backend

Простое Django/DRF API для LMS с курсами, уроками и кастомным пользователем на email.

## Быстрый старт
- Установить зависимости: `poetry install`
- Создать `.env` на основе `env.example`
- Применить миграции: `poetry run python manage.py migrate`
- Запустить сервер: `poetry run python manage.py runserver`
- (Опционально) наполнить демо-данными: `poetry run python manage.py seed_payments`
- Создать группу модераторов: `poetry run python manage.py seed_groups`

## API Документация
- **Swagger UI**: `http://127.0.0.1:8000/api/docs/`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/`
- **OpenAPI Schema**: `http://127.0.0.1:8000/api/schema/`

## Основные эндпоинты
- `POST /admin/` — стандартная админка (создайте суперпользователя `poetry run python manage.py createsuperuser`)
- `GET|POST /api/courses/` и `GET|PATCH|DELETE /api/courses/<id>/` — CRUD курсов (ViewSet, возвращает `lessons_count`, вложенные `lessons` и флаг `is_subscribed`)
- `GET|POST /api/lessons/` и `GET|PATCH|DELETE /api/lessons/<id>/` — CRUD уроков (generics, с пагинацией)
- `POST /api/subscriptions/` — управление подпиской на курс (`{"course_id": <id>}`)
- Платежи:
  - `GET /api/payments/` — список платежей с фильтрами (`paid_course`, `paid_lesson`, `payment_method`) и сортировкой по `payment_date`
  - `POST /api/payments/create/` — создание платежа через Stripe (`{"paid_course": <id>, "amount": <сумма>}` или `{"paid_lesson": <id>, "amount": <сумма>}`)
  - `GET /api/payments/<id>/status/` — проверка статуса платежа
- Пользователи:
  - Регистрация: `POST /api/auth/register/` (доступно без авторизации)
  - JWT: `POST /api/auth/token/`, `POST /api/auth/token/refresh/`
  - Профиль: `GET|PATCH /api/users/<id>/`
  - CRUD: `/api/users/` (список — только админ; карточка — владелец или админ)

## Особенности
- **Валидация ссылок**: В уроках и курсах разрешены только ссылки на YouTube. Ссылки на сторонние ресурсы в описаниях запрещены.
- **Подписки**: Пользователи могут подписываться на курсы. Флаг `is_subscribed` отображается в сериализаторе курса.
- **Пагинация**: Курсы и уроки используют пагинацию (по умолчанию 10 элементов на страницу, максимум 50). Используйте параметры `?page=1&page_size=20`.
- **Права доступа**: Все эндпоинты (кроме регистрации и JWT) требуют авторизации (Bearer JWT). Модераторы могут читать/редактировать любые курсы и уроки, но не могут их создавать и удалять. Обычные пользователи работают только со своими курсами/уроками.
- **Оплата через Stripe**: Интеграция со Stripe для оплаты курсов и уроков. При создании платежа автоматически создаются продукт и цена в Stripe, возвращается ссылка на оплату. Для тестирования используйте тестовые карты из [документации Stripe](https://stripe.com/docs/terminal/references/testing#standard-test-cards).

## Настройка Stripe
1. Зарегистрируйтесь на [Stripe Dashboard](https://dashboard.stripe.com/register)
2. Получите API ключи из раздела "Developers" → "API keys"
3. Добавьте ключи в `.env`:
   ```
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PUBLISHABLE_KEY=pk_test_...
   ```
4. Для тестирования используйте тестовые карты (например, `4242 4242 4242 4242` с любой будущей датой и CVC)

## Тестирование
Запустите тесты: `poetry run python manage.py test lms.tests`

Используйте Postman/HTTPie с JWT-токеном: `Authorization: Bearer <access_token>`.



