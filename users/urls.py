from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.payment_views import PaymentCreateView, PaymentStatusView
from users.views import PaymentListView, UserProfileView, UserRegisterView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("payments/create/", PaymentCreateView.as_view(), name="payment-create"),
    path("payments/<int:pk>/status/", PaymentStatusView.as_view(), name="payment-status"),
    path("users/<int:pk>/", UserProfileView.as_view(), name="user-profile"),
    path("auth/register/", UserRegisterView.as_view(), name="user-register"),
]

