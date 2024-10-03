from django.contrib import admin
from django.core.checks import messages

from train.models import Seat
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['user', 'passenger', 'route', 'seat',  'is_active']
    list_display = ['passenger', 'route', 'seat', 'is_active']
    actions = ['set_active', 'set_inactive']

    @admin.action(description="Установить активными")
    def set_active(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"Сделано активными записей: {count}")

    @admin.action(description="Установить неактивными")
    def set_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"Сделано неактивными записей: {count}", messages.WARNING)
