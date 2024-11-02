from django.db import models
from users.models import User, Passenger
from route.models import Route
from train.models import Seat


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='orders', verbose_name='Пассажир')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='orders', verbose_name='Маршрут')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='orders', verbose_name='Место')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    purchase_date = models.DateTimeField(auto_now=True, verbose_name='Дата покупки')
    price = models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Цена')

    def __str__(self):
        return f"Заказ: {self.user} {self.route}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
