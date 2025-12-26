from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import (
    YouTubeURLValidator,
    validate_no_external_links,
    validate_youtube_url,
)


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")
    video_url = serializers.URLField(validators=[validate_youtube_url], required=False, allow_blank=True)
    description = serializers.CharField(validators=[validate_no_external_links], required=False, allow_blank=True)

    class Meta:
        model = Lesson
        fields = ["id", "owner", "course", "title", "description", "preview", "video_url"]
        read_only_fields = ["id", "owner"]
        validators = [YouTubeURLValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    description = serializers.CharField(validators=[validate_no_external_links], required=False, allow_blank=True)

    class Meta:
        model = Course
        fields = ["id", "owner", "title", "description", "preview", "lessons_count", "lessons", "is_subscribed"]
        read_only_fields = ["id", "owner", "lessons_count", "lessons", "is_subscribed"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False



