from django.contrib import admin
from django.core.checks import messages

from .models import DiscountCard


@admin.register(DiscountCard)
class DiscountCardAdmin(admin.ModelAdmin):
    fields = ['user', 'max_usage', 'discount', 'duration', 'types_of_trains']
    list_display = ['user', 'max_usage', 'discount', 'duration', 'is_active']
    actions = ['set_active', 'set_inactive']

    @admin.action(description="Установить активными")
    def set_active(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"Сделано активными записей: {count}")

    @admin.action(description="Установить неактивными")
    def set_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"Сделано неактивными записей: {count}", messages.WARNING)
