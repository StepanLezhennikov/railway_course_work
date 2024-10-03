from django.core.exceptions import ValidationError
from django.db import models
from train.models import Train
from .validators import validate_first_letter_uppercase


class Station(models.Model):
    name = models.CharField(max_length=255, validators=[validate_first_letter_uppercase],
                            verbose_name='Название станции')
    city = models.CharField(max_length=255, validators=[validate_first_letter_uppercase], verbose_name='Город')
    country = models.CharField(max_length=255, validators=[validate_first_letter_uppercase], verbose_name='Страна')

    def __str__(self):
        return f'Станция {self.name}'

    class Meta:
        verbose_name = "Станция"
        verbose_name_plural = "Станции"


class Route(models.Model):
    from_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='from_route',
                                     verbose_name='Откуда')
    to_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='to_route', verbose_name='Куда')
    departure_time = models.DateTimeField(verbose_name='Время отправления')
    arrival_time = models.DateTimeField(verbose_name='Время прибытия')
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='routes', verbose_name='Поезд')
    starting_price = models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Начальная цена')

    def __str__(self):
        return f'Маршрут {self.from_station.name} -> {self.to_station.name}'

    def clean(self):
        super().clean()
        check, route = self.train.check_train_available(self.departure_time, self.arrival_time)
        if not check:
            raise ValidationError(f'Этот поезд занят в это время на иаршруте: {route[0][0]}-{route[0][1]}')

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"


class Stop(models.Model):
    stop_number = models.IntegerField(default=0, blank=True, verbose_name='Номер остановки')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops', verbose_name='Маршрут')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='stops', verbose_name='Станция')
    arrival_time = models.DateTimeField(verbose_name='Время прибытия')
    departure_time = models.DateTimeField(verbose_name='Время отправления')

    def __str__(self):
        return f"Остановка: {self.station} | {self.route}"

    class Meta:
        verbose_name = "Остановка"
        verbose_name_plural = "Остановки"
        constraints = [
            models.UniqueConstraint(fields=['stop_number', 'route'], name='unique_stop_number_route')
        ]
