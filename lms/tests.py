from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription

User = get_user_model()


def get_full_url(url_name, **kwargs):
    """Вспомогательная функция для получения полного URL с префиксом /api/"""
    return f"/api{reverse(url_name, kwargs=kwargs)}"


class LessonCRUDTestCase(APITestCase):
    """Тесты для CRUD операций с уроками"""

    def setUp(self):
        """Подготовка тестовых данных"""
        # Создаем пользователей
        self.owner_user = User.objects.create_user(
            email="owner@test.com",
            password="testpass123"
        )
        self.other_user = User.objects.create_user(
            email="other@test.com",
            password="testpass123"
        )
        self.moderator_user = User.objects.create_user(
            email="moderator@test.com",
            password="testpass123"
        )
        
        # Создаем группу модераторов и добавляем пользователя
        moderators_group, _ = Group.objects.get_or_create(name="moderators")
        self.moderator_user.groups.add(moderators_group)
        
        # Создаем курс и урок
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            owner=self.owner_user
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            description="Test Lesson Description",
            video_url="https://www.youtube.com/watch?v=test",
            owner=self.owner_user
        )

    def test_create_lesson(self):
        """Тест создания урока владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lesson-list")
        data = {
            "course": self.course.id,
            "title": "New Lesson",
            "description": "New Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=new"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.get(title="New Lesson").owner, self.owner_user)

    def test_create_lesson_by_moderator_forbidden(self):
        """Тест запрета создания урока модератором"""
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lesson-list")
        data = {
            "course": self.course.id,
            "title": "Moderator Lesson",
            "description": "Moderator Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=mod"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_lessons_owner(self):
        """Тест получения списка уроков владельцем (видит только свои)"""
        # Создаем урок другого пользователя
        other_course = Course.objects.create(
            title="Other Course",
            owner=self.other_user
        )
        Lesson.objects.create(
            course=other_course,
            title="Other Lesson",
            owner=self.other_user
        )
        
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)  # Только свой урок
        self.assertEqual(response.data["results"][0]["title"], "Test Lesson")

    def test_list_lessons_moderator(self):
        """Тест получения списка уроков модератором (видит все)"""
        # Создаем урок другого пользователя
        other_course = Course.objects.create(
            title="Other Course",
            owner=self.other_user
        )
        Lesson.objects.create(
            course=other_course,
            title="Other Lesson",
            owner=self.other_user
        )
        
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # Все уроки

    def test_retrieve_lesson_owner(self):
        """Тест получения урока владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Lesson")

    def test_retrieve_lesson_other_user_forbidden(self):
        """Тест запрета получения чужого урока"""
        self.client.force_authenticate(user=self.other_user)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_lesson_owner(self):
        """Тест обновления урока владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        data = {"title": "Updated Lesson"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_update_lesson_moderator(self):
        """Тест обновления урока модератором"""
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        data = {"title": "Updated by Moderator"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated by Moderator")

    def test_update_lesson_other_user_forbidden(self):
        """Тест запрета обновления чужого урока"""
        self.client.force_authenticate(user=self.other_user)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        data = {"title": "Hacked Lesson"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_lesson_owner(self):
        """Тест удаления урока владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_delete_lesson_moderator_forbidden(self):
        """Тест запрета удаления урока модератором"""
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_other_user_forbidden(self):
        """Тест запрета удаления чужого урока"""
        self.client.force_authenticate(user=self.other_user)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_youtube_url_validation(self):
        """Тест валидации YouTube ссылок"""
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lesson-list")
        # Пытаемся создать урок с не-YouTube ссылкой
        data = {
            "course": self.course.id,
            "title": "Invalid URL Lesson",
            "video_url": "https://example.com/video"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("youtube.com", str(response.data))

    def test_external_links_in_description_validation(self):
        """Тест валидации внешних ссылок в описании"""
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lesson-list")
        # Пытаемся создать урок с внешней ссылкой в описании
        data = {
            "course": self.course.id,
            "title": "Lesson with External Link",
            "description": "Check this out: https://example.com/learn"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("сторонние ресурсы", str(response.data))

    def test_youtube_link_in_description_allowed(self):
        """Тест что YouTube ссылки в описании разрешены"""
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lesson-list")
        # Создаем урок с YouTube ссылкой в описании
        data = {
            "course": self.course.id,
            "title": "Lesson with YouTube Link",
            "description": "Watch this: https://www.youtube.com/watch?v=test"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SubscriptionTestCase(APITestCase):
    """Тесты для функционала подписки на курс"""

    def setUp(self):
        """Подготовка тестовых данных"""
        # Создаем пользователей
        self.user1 = User.objects.create_user(
            email="user1@test.com",
            password="testpass123"
        )
        self.user2 = User.objects.create_user(
            email="user2@test.com",
            password="testpass123"
        )
        
        # Создаем курсы
        self.course1 = Course.objects.create(
            title="Course 1",
            description="Description 1",
            owner=self.user1
        )
        self.course2 = Course.objects.create(
            title="Course 2",
            description="Description 2",
            owner=self.user2
        )

    def test_create_subscription(self):
        """Тест создания подписки"""
        self.client.force_authenticate(user=self.user1)
        url = reverse("subscription")
        data = {"course_id": self.course1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("подписка добавлена", response.data["message"])
        self.assertTrue(
            Subscription.objects.filter(user=self.user1, course=self.course1).exists()
        )

    def test_delete_subscription(self):
        """Тест удаления подписки"""
        # Создаем подписку
        Subscription.objects.create(user=self.user1, course=self.course1)
        
        self.client.force_authenticate(user=self.user1)
        url = reverse("subscription")
        data = {"course_id": self.course1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("подписка удалена", response.data["message"])
        self.assertFalse(
            Subscription.objects.filter(user=self.user1, course=self.course1).exists()
        )

    def test_subscription_flag_in_course_serializer(self):
        """Тест отображения флага подписки в сериализаторе курса"""
        # Создаем подписку
        Subscription.objects.create(user=self.user1, course=self.course1)
        
        self.client.force_authenticate(user=self.user1)
        url = reverse("course-detail", kwargs={"pk": self.course1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_subscribed"])

    def test_subscription_flag_false_when_not_subscribed(self):
        """Тест отображения флага подписки когда пользователь не подписан"""
        self.client.force_authenticate(user=self.user1)
        url = reverse("course-detail", kwargs={"pk": self.course1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_subscribed"])

    def test_subscription_requires_authentication(self):
        """Тест требования аутентификации для подписки"""
        url = reverse("subscription")
        data = {"course_id": self.course1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscription_missing_course_id(self):
        """Тест обработки отсутствия course_id"""
        self.client.force_authenticate(user=self.user1)
        url = reverse("subscription")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
