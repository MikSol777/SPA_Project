from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Lesson
        fields = ["id", "owner", "course", "title", "description", "preview", "video_url"]
        read_only_fields = ["id", "owner"]


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "owner", "title", "description", "preview", "lessons_count", "lessons"]
        read_only_fields = ["id", "owner", "lessons_count", "lessons"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()



