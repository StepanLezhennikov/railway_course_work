from django.db import models
from users.models import User, Passenger
from route.models import Route
from train.models import Train, Car, Seat


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='orders')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='orders')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='orders')
    is_active = models.BooleanField(default=True)
    # price = models.DecimalField()

    def __str__(self):
        return f"Заказ: {self.user} {self.route}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
