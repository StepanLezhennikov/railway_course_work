from django.contrib import admin

from train.models import Car, Train, Seat


# @admin.register(Seat)
# class SeatAdmin(admin.ModelAdmin):
#     fields = ['number', 'is_occupied', 'car']


# @admin.register(Car)
# class CarAdmin(admin.ModelAdmin):
#     fields = ['number', 'type', 'capacity']
#     search_fields = ['type']


class CarInline(admin.TabularInline):
    model = Car
    extra = 1


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    inlines = [CarInline]
    fields = ['number', 'type']
    list_display = ['number', 'type']
    search_fields = ['number']
