from django.db import models
from django.contrib.auth.models import AbstractUser


class Passenger(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    second_name = models.CharField(max_length=255, verbose_name='Фамилия')
    fathername = models.CharField(max_length=255, blank=True, verbose_name='Отчество')
    passport_number = models.CharField(max_length=10, verbose_name='Номер паспорта')
    is_child = models.BooleanField(default=False, verbose_name='Является ребенком')

    def __str__(self):
        return f"{self.second_name} {self.first_name} {self.fathername}"


class User(AbstractUser):
    passengers = models.ManyToManyField(Passenger, related_name='user', blank=True, verbose_name='Пассажиры')
    phone_number = models.CharField(blank=True, max_length=15)
