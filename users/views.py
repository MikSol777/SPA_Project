from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.select_related("user", "paid_course", "paid_lesson").all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]
