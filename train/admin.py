from django.contrib import admin

from train.models import Car, Train, Seat


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    fields = ['number', 'is_occupied', 'car']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    fields = ['number', 'type', 'capacity']


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    fields = ['number', 'type', 'cars']


