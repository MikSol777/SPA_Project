from django.core.management.base import BaseCommand
from django.utils import timezone

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Seed sample user, course, lesson, and payments data"

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(
            email="demo@example.com",
            defaults={"first_name": "Demo", "last_name": "User", "is_active": True},
        )
        if not user.password:
            user.set_password("password123")
            user.save()

        course, _ = Course.objects.get_or_create(
            title="Demo Course",
            defaults={"description": "Sample course for payments seed"},
        )

        lesson, _ = Lesson.objects.get_or_create(
            course=course,
            title="Intro Lesson",
            defaults={"description": "Sample lesson", "video_url": "https://example.com/video"},
        )

        Payment.objects.get_or_create(
            user=user,
            paid_course=course,
            paid_lesson=None,
            amount=1000.00,
            payment_method=Payment.PaymentMethod.CASH,
            defaults={"payment_date": timezone.now()},
        )

        Payment.objects.get_or_create(
            user=user,
            paid_course=None,
            paid_lesson=lesson,
            amount=250.00,
            payment_method=Payment.PaymentMethod.TRANSFER,
            defaults={"payment_date": timezone.now()},
        )

        self.stdout.write(self.style.SUCCESS("Seeded demo payments data"))










