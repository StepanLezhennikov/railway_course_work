from django.db import models
from train.models import Train


class Station(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f'Станция {self.name}'

    class Meta:
        verbose_name = "Станция"
        verbose_name_plural = "Станции"


class Route(models.Model):
    from_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='from_route')
    to_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='to_route')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='routes')
    # starting_price = models.DecimalField()
    
    def __str__(self):
        return f'Маршрут {self.from_station.name} -> {self.to_station.name}'

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"


class Stop(models.Model):
    stop_number = models.IntegerField(default=0, blank=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='stops')
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    def __str__(self):
        return f"Остановка: {self.station} | {self.route}"

    class Meta:
        verbose_name = "Остановка"
        verbose_name_plural = "Остановки"
        constraints = [
            models.UniqueConstraint(fields=['stop_number', 'route'], name='unique_stop_number_route')
        ]

