from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.db import connection

CarTypes = [
    ("Плацкарт", "Плацкарт"),
    ("Купе", "Купе"),
    ("Сидячий", "Сидячий"),
]


class TrainType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Тип поезда")

    def __str__(self):
        return self.name


class Train(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name='Номер поезда')
    type = models.ForeignKey(TrainType, on_delete=models.CASCADE, verbose_name='Тип')

    def __str__(self):
        return f"Поезд {self.type} №{self.number}"

    def check_train_available(self, departure_time, arrival_time):
        # from route.models import Route
        # routes = Route.objects.filter(
        #     Q(train__pk=self.pk) & (
        #             Q(departure_time__lte=arrival_time) & Q(arrival_time__gte=departure_time)
        #     )
        # )
        with connection.cursor() as cursor:
            query = """
            SELECT st_from.name AS from_station, st_to.name AS to_station 
            FROM route_route AS r
            JOIN route_station AS st_from ON st_from.id = r.from_station_id 
            JOIN route_station AS st_to ON st_to.id = r.to_station_id 
            WHERE r.train_id = %s
            AND (r.departure_time <= %s AND r.arrival_time >= %s)
            """
            cursor.execute(query, [self.pk, arrival_time, departure_time])
            routes = cursor.fetchall()

        if routes:
            return False, routes
        return True, routes

    class Meta:
        verbose_name = "Поезд"
        verbose_name_plural = "Поезда"


class Car(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='cars', verbose_name='Поезд')
    number = models.PositiveIntegerField(verbose_name='Номер')
    type = models.CharField(max_length=50, choices=CarTypes, verbose_name='Тип')
    capacity = models.IntegerField(verbose_name='Количество мест')

    def __str__(self):
        return f"Вагон {self.type} №{self.number} | {self.train}"

    class Meta:
        verbose_name = "Вагон"
        verbose_name_plural = "Вагоны"
        unique_together = ('train', 'number')


@receiver(post_save, sender=Car)
def create_seats(sender, instance, created, **kwargs):
    if created:
        for s in range(instance.capacity):
            # Seat.objects.create(car=instance, number=s + 1)
            with connection.cursor() as cursor:
                query = """
                        INSERT INTO train_seat(number, is_occupied, car_id) VALUES(%s, %s, %s);
                        """
                cursor.execute(query, [s + 1, False, instance.id])


class Seat(models.Model):
    number = models.IntegerField(verbose_name='Номер')
    is_occupied = models.BooleanField(default=False, verbose_name='Занято')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='seats', null=True, verbose_name='Вагон')

    def __str__(self):
        return f"Место №{self.number} в вагоне {self.car.number}"

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"


@receiver(pre_delete, sender=Train)
def delete_cars_with_train(sender, instance, **kwargs):
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT id FROM train_car WHERE train_id = %s            
        """, [instance.id])
        car_ids = cursor.fetchall()
        car_ids = [car_id[0] for car_id in car_ids]

        for car_id in car_ids:
            cursor.execute("""
                DELETE FROM train_seat
                WHERE car_id = %s   
                """, [car_id])

        # cursor.execute("DELETE FROM train_train_cars WHERE train_id = %s", [instance.id])

        for car_id in car_ids:
            cursor.execute("""
                DELETE FROM train_car
                WHERE id = %s   
                """, [car_id])
