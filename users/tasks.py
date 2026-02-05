from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task
def deactivate_inactive_users() -> int:
    """
    Деактивирует пользователей, которые не заходили более месяца.

    Основано на поле last_login и флаге is_active.
    Возвращает количество деактивированных пользователей.
    """
    User = get_user_model()
    threshold = timezone.now() - timedelta(days=30)

    # last_login может быть None для никогда не заходивших пользователей – их не трогаем
    qs = User.objects.filter(is_active=True, last_login__lt=threshold)
    updated = qs.update(is_active=False)
    return updated

