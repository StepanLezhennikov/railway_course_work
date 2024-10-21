from django.db import models

from discount.validators import between_0_and_1
from train.models import TrainType
from users.models import User


class DiscountCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    amount_of_rides = models.IntegerField(blank=True, default=0, verbose_name="Количество поездок")
    discount = models.DecimalField(max_digits=5, decimal_places=2, validators=[between_0_and_1], verbose_name="Процент скидки")
    duration = models.DurationField(verbose_name="Время действия")
    types_of_trains = models.ManyToManyField(TrainType, verbose_name='Тип поездов')
    max_usage = models.IntegerField(null=True, blank=True, verbose_name="Максимальное количество поездок")
    is_active = models.BooleanField(blank=True, default=True, verbose_name="Активна ли карта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f'Карта пользователя {self.user.username}, скидка: {self.discount}'

    def save(self, *args, **kwargs):
        if not self.amount_of_rides:
            self.amount_of_rides = self.max_usage
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Скидочная карта"
        verbose_name_plural = "Скидочные карты"
