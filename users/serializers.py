from rest_framework import serializers

from lms.models import Course, Lesson
from users.models import Payment, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "city", "avatar"]
        read_only_fields = ["id", "email"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "first_name", "last_name", "phone", "city", "avatar"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(UserSerializer):
    pass


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
            "payment_status",
            "stripe_product_id",
            "stripe_price_id",
            "stripe_session_id",
            "payment_url",
        ]
        read_only_fields = [
            "id",
            "payment_date",
            "payment_status",
            "stripe_product_id",
            "stripe_price_id",
            "stripe_session_id",
            "payment_url",
        ]


class PaymentCreateSerializer(serializers.Serializer):
    """Сериализатор для создания платежа"""
    paid_course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), required=False, allow_null=True
    )
    paid_lesson = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(), required=False, allow_null=True
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, attrs):
        if not attrs.get("paid_course") and not attrs.get("paid_lesson"):
            raise serializers.ValidationError("Необходимо указать либо курс, либо урок")
        if attrs.get("paid_course") and attrs.get("paid_lesson"):
            raise serializers.ValidationError("Укажите либо курс, либо урок, но не оба одновременно")
        return attrs

