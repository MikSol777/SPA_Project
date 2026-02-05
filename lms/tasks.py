from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from lms.models import Course, Subscription


@shared_task
def send_course_update_notification(course_id: int) -> int:
    """
    Отправляет письма пользователям, подписанным на обновление конкретного курса.

    Возвращает количество получателей.
    """
    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(course=course).select_related("user")

    recipients = [sub.user.email for sub in subscriptions if sub.user.email]
    if not recipients:
        return 0

    subject = f"Обновление курса: {course.title}"
    message = (
        f"Курс «{course.title}» был обновлён. "
        "Зайдите в личный кабинет, чтобы посмотреть новые материалы."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=True,
    )

    return len(recipients)

