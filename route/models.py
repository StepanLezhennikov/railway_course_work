from django.db import models


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

    def __str__(self):
        return f'Маршрут {self.from_station.name} -> {self.to_station.name}'

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"


class Stop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='stops')
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    def __str__(self):
        return f"Остановка: {self.station} | {self.route}"

    class Meta:
        verbose_name = "Остановка"
        verbose_name_plural = "Остановки"
