from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import Payment, User
from users.permissions import IsModerator, IsSelfOrAdmin
from users.serializers import (
    PaymentSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Payment.objects.select_related("user", "paid_course", "paid_lesson").all()
        user = self.request.user
        if IsModerator().has_permission(self.request, self):
            return qs
        return qs.filter(user=user)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsSelfOrAdmin]


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            # registration could also use this path
            self.permission_classes = [AllowAny]
        elif self.action == "list":
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsSelfOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]
