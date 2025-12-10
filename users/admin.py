from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Payment, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "phone", "city", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "city")
    ordering = ("email",)
    search_fields = ("email", "phone", "city")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone", "city", "avatar")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "payment_date", "paid_course", "paid_lesson", "amount", "payment_method")
    list_filter = ("payment_method", "payment_date")
    search_fields = ("user__email", "paid_course__title", "paid_lesson__title")
