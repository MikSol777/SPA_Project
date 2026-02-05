# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Ожидает оплаты'), ('paid', 'Оплачено'), ('cancelled', 'Отменено')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='payment',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='stripe_price_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='stripe_session_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Наличные'), ('transfer', 'Перевод на счет'), ('stripe', 'Stripe')], default='cash', max_length=20),
        ),
    ]









