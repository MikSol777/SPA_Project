"""
Сервисные функции для работы со Stripe API
"""
import stripe
from django.conf import settings

# Инициализация Stripe API ключа
if settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name: str, description: str = "") -> dict:
    """
    Создает продукт в Stripe
    
    Args:
        name: Название продукта
        description: Описание продукта
        
    Returns:
        dict: Данные созданного продукта
    """
    try:
        product = stripe.Product.create(
            name=name,
            description=description,
        )
        return product
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании продукта в Stripe: {str(e)}")


def create_stripe_price(product_id: str, amount: float, currency: str = "usd") -> dict:
    """
    Создает цену в Stripe
    
    Args:
        product_id: ID продукта в Stripe
        amount: Сумма в долларах (будет преобразована в центы)
        currency: Валюта (по умолчанию USD)
        
    Returns:
        dict: Данные созданной цены
    """
    try:
        # Преобразуем сумму в центы (копейки)
        amount_cents = int(amount * 100)
        
        price = stripe.Price.create(
            product=product_id,
            unit_amount=amount_cents,
            currency=currency,
        )
        return price
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании цены в Stripe: {str(e)}")


def create_stripe_session(price_id: str, success_url: str, cancel_url: str) -> dict:
    """
    Создает сессию оплаты в Stripe
    
    Args:
        price_id: ID цены в Stripe
        success_url: URL для перенаправления после успешной оплаты
        cancel_url: URL для перенаправления при отмене оплаты
        
    Returns:
        dict: Данные созданной сессии
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании сессии в Stripe: {str(e)}")


def retrieve_stripe_session(session_id: str) -> dict:
    """
    Получает информацию о сессии оплаты в Stripe
    
    Args:
        session_id: ID сессии в Stripe
        
    Returns:
        dict: Данные сессии
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при получении сессии из Stripe: {str(e)}")

