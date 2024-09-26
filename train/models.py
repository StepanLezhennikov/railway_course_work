from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db import connection

CarTypes = [
    ("Плацкарт", "Плацкарт"),
    ("Купе", "Купе"),
    ("Сидячий", "Сидячий"),
]

TrainTypes = [
    ("Скоростной", "Скоростной"),
    ("Междугородний", "Междугородний"),
    ("Пригородный", "Пригородный"),
]


class Train(models.Model):
    number = models.IntegerField(unique=True)
    type = models.CharField(max_length=50, choices=TrainTypes)
    cars = models.ManyToManyField('Car', related_name='train')

    def __str__(self):
        return f"Поезд {self.type} №{self.number}"

    class Meta:
        verbose_name = "Поезд"
        verbose_name_plural = "Поезда"


class Car(models.Model):
    number = models.IntegerField()
    type = models.CharField(max_length=50, choices=CarTypes)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Вагон {self.type} №{self.number}"

    class Meta:
        verbose_name = "Вагон"
        verbose_name_plural = "Вагоны"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for s in range(self.capacity):
            Seat.objects.create(car=self, number=s + 1)


class Seat(models.Model):
    number = models.IntegerField()
    is_occupied = models.BooleanField(default=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='seats', null=True)

    def __str__(self):
        return f"Место №{self.number} в вагоне {self.car.number}"

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"


@receiver(pre_delete, sender=Train)
def delete_cars_with_train(sender, instance, **kwargs):
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT car_id FROM train_train_cars WHERE train_id = %s            
        """, [instance.id])
        car_ids = cursor.fetchall()
        car_ids = [car_id[0] for car_id in car_ids]

        for car_id in car_ids:
            cursor.execute("""
                DELETE FROM train_seat
                WHERE car_id = %s   
                """, [car_id])

        cursor.execute("DELETE FROM train_train_cars WHERE train_id = %s", [instance.id])

        for car_id in car_ids:
            cursor.execute("""
                DELETE FROM train_car
                WHERE id = %s   
                """, [car_id])
