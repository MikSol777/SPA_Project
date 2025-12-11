from django.urls import path

from users.views import PaymentListView, UserProfileView

urlpatterns = [
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("users/<int:pk>/", UserProfileView.as_view(), name="user-profile"),
]

