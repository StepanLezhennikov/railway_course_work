from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

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
    number = models.IntegerField()
    type = models.CharField(max_length=50, choices=TrainTypes)
    cars = models.ManyToManyField('Car', related_name='train')

    def __str__(self):
        return f"Поезд {self.type} №{self.number}"


class Car(models.Model):
    number = models.IntegerField()
    type = models.CharField(max_length=50, choices=CarTypes)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Вагон {self.type} №{self.number}"

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


@receiver(pre_delete, sender=Train)
def delete_cars_with_train(sender, instance, **kwargs):
    instance.cars.all().delete()
