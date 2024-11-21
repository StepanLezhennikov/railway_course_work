from datetime import datetime

from django.db import models

from discount.validators import between_0_and_1
from train.models import TrainType
from users.models import User

class DiscountCardType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Цена')
    discount = models.DecimalField(max_digits=5, decimal_places=2, validators=[between_0_and_1],
                                   verbose_name="Процент скидки")
    duration = models.DurationField(verbose_name="Время действия")
    types_of_trains = models.ManyToManyField(TrainType, verbose_name='Тип поездов')
    max_usage = models.IntegerField(null=True, blank=True, verbose_name="Максимальное количество поездок")
    is_active = models.BooleanField(blank=True, default=True, verbose_name="Активна ли карта")


    def __str__(self):
        return f"{self.name}: {self.discount} на {self.duration}"

    class Meta:
        verbose_name = "Тип скидочной карты"
        verbose_name_plural = "Типы скидочных карт"



class DiscountCard(models.Model):
    type = models.ForeignKey(DiscountCardType, on_delete=models.CASCADE, verbose_name='Тип скидочной карты', related_name='discount_cards')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name='discounts')
    amount_of_rides = models.IntegerField(blank=True, default=0, verbose_name="Количество поездок")
    end_date = models.DateField(blank=True, verbose_name="Дата окончания действия")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f'Карта {self.type.name} пользователя {self.user.username}, скидка: {self.type.discount}'

    def save(self, *args, **kwargs):
        if not self.amount_of_rides and not self.end_date:
            self.amount_of_rides = self.type.max_usage
            self.end_date = datetime.now() + self.type.duration
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Скидочная карта"
        verbose_name_plural = "Скидочные карты"
