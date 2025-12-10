from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "course", "title", "description", "preview", "video_url"]
        read_only_fields = ["id"]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "lessons_count", "lessons"]
        read_only_fields = ["id", "lessons_count", "lessons"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()



