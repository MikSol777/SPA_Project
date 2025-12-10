from rest_framework import serializers

from users.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "amount",
            "payment_method",
        ]
        read_only_fields = ["id", "payment_date"]

