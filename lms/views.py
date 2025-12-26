from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginators import CourseLessonPagination
from lms.permissions import IsCourseOwner, IsLessonOwner, IsOwnerOrModerator
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, MODERATOR_GROUP



class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPagination

    def get_queryset(self):
        qs = Course.objects.all()
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name=MODERATOR_GROUP).exists():
            return qs
        return qs.filter(owner=user)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action == "create":
            # Только аутентифицированные и не-модераторы создают
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        elif self.action == "destroy":
            # Модераторам удалять нельзя, только владельцам
            self.permission_classes = [IsAuthenticated, IsCourseOwner, ~IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def get_serializer_context(self):
        """Передаем request в контекст сериализатора для проверки подписки"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CourseLessonPagination

    def get_queryset(self):
        qs = Lesson.objects.all()
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name=MODERATOR_GROUP).exists():
            return qs
        return qs.filter(owner=user)

    def get_permissions(self):
        if self.request.method.lower() == "post":
            return [IsAuthenticated(), ~IsModerator()]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_queryset(self):
        qs = Lesson.objects.all()
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name=MODERATOR_GROUP).exists():
            return qs
        return qs.filter(owner=user)

    def get_permissions(self):
        if self.request.method.lower() == "delete":
            return [IsAuthenticated(), IsLessonOwner(), ~IsModerator()]
        return super().get_permissions()

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionAPIView(APIView):
    """Эндпоинт для управления подпиской на курс"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        
        if not course_id:
            return Response(
                {"error": "course_id обязателен"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        course = get_object_or_404(Course, id=course_id)
        subscription, created = Subscription.objects.get_or_create(
            user=user,
            course=course
        )
        
        if not created:
            # Подписка уже существует - удаляем
            subscription.delete()
            message = "подписка удалена"
        else:
            # Подписка создана
            message = "подписка добавлена"
        
        return Response({"message": message}, status=status.HTTP_200_OK)
