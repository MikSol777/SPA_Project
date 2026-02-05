from django.db import models


class Course(models.Model):
    owner = models.ForeignKey(
        "users.User", related_name="courses", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to="courses/", blank=True, null=True)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    owner = models.ForeignKey("users.User", related_name="lessons", on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to="lessons/", blank=True, null=True)
    video_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """Модель подписки пользователя на курс"""
    user = models.ForeignKey("users.User", related_name="subscriptions", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="subscriptions", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["user", "course"]]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}"
