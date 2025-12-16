from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from lms.models import Course, Lesson
from lms.permissions import IsCourseOwner, IsLessonOwner, IsOwnerOrModerator
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, MODERATOR_GROUP


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

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
