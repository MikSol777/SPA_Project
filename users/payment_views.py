"""
Views для работы с платежами через Stripe
"""
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from lms.models import Course, Lesson
from users.models import Payment
from users.serializers import PaymentCreateSerializer, PaymentSerializer
from users.services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
    retrieve_stripe_session,
)


class PaymentCreateView(generics.CreateAPIView):
    """
    Создание платежа через Stripe
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentCreateSerializer

    @extend_schema(
        summary="Создать платеж через Stripe",
        description="Создает платеж для курса или урока через Stripe. "
                    "Возвращает ссылку на оплату.",
        request=PaymentCreateSerializer,
        responses={201: PaymentSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        paid_course_id = serializer.validated_data.get("paid_course")
        paid_lesson_id = serializer.validated_data.get("paid_lesson")
        amount = serializer.validated_data.get("amount")
        
        # Проверяем, что указан либо курс, либо урок
        if not paid_course_id and not paid_lesson_id:
            return Response(
                {"error": "Необходимо указать либо курс, либо урок"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if paid_course_id and paid_lesson_id:
            return Response(
                {"error": "Укажите либо курс, либо урок, но не оба одновременно"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Получаем объект курса или урока
        if paid_course_id:
            course_or_lesson = get_object_or_404(Course, id=paid_course_id)
            name = course_or_lesson.title
            description = course_or_lesson.description or ""
        else:
            course_or_lesson = get_object_or_404(Lesson, id=paid_lesson_id)
            name = course_or_lesson.title
            description = course_or_lesson.description or ""
        
        try:
            # Создаем продукт в Stripe
            product = create_stripe_product(name=name, description=description)
            
            # Создаем цену в Stripe
            price = create_stripe_price(
                product_id=product.id,
                amount=float(amount)
            )
            
            # Формируем URL для перенаправления
            base_url = request.build_absolute_uri("/")
            success_url = f"{base_url}api/payments/success/"
            cancel_url = f"{base_url}api/payments/cancel/"
            
            # Создаем сессию оплаты в Stripe
            session = create_stripe_session(
                price_id=price.id,
                success_url=success_url,
                cancel_url=cancel_url
            )
            
            # Создаем платеж в нашей системе
            payment = Payment.objects.create(
                user=user,
                paid_course=course_or_lesson if isinstance(course_or_lesson, Course) else None,
                paid_lesson=course_or_lesson if isinstance(course_or_lesson, Lesson) else None,
                amount=amount,
                payment_method=Payment.PaymentMethod.STRIPE,
                payment_status=Payment.PaymentStatus.PENDING,
                stripe_product_id=product.id,
                stripe_price_id=price.id,
                stripe_session_id=session.id,
                payment_url=session.url,
            )
            
            # Возвращаем данные платежа со ссылкой на оплату
            response_serializer = PaymentSerializer(payment)
            return Response(
                {
                    **response_serializer.data,
                    "payment_url": session.url,
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentStatusView(generics.RetrieveAPIView):
    """
    Проверка статуса платежа через Stripe
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    @extend_schema(
        summary="Проверить статус платежа",
        description="Проверяет статус платежа через Stripe API",
        responses={200: PaymentSerializer},
    )
    def get(self, request, *args, **kwargs):
        payment = self.get_object()
        
        # Проверяем, что платеж принадлежит текущему пользователю
        if payment.user != request.user:
            return Response(
                {"error": "Доступ запрещен"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Если есть session_id, проверяем статус в Stripe
        if payment.stripe_session_id:
            try:
                session = retrieve_stripe_session(payment.stripe_session_id)
                
                # Обновляем статус платежа на основе статуса сессии
                if session.payment_status == "paid":
                    payment.payment_status = Payment.PaymentStatus.PAID
                elif session.payment_status == "unpaid":
                    payment.payment_status = Payment.PaymentStatus.PENDING
                else:
                    payment.payment_status = Payment.PaymentStatus.CANCELLED
                
                payment.save()
                
            except Exception as e:
                return Response(
                    {"error": f"Ошибка при проверке статуса: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)









