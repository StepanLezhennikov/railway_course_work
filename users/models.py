from django.db import models
from django.contrib.auth.models import AbstractUser


class Passenger(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    fathername = models.CharField(max_length=255, blank=True)
    passport_number = models.CharField(max_length=10)
    is_child = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.surname} {self.name} {self.fathername}"


class User(AbstractUser):
    passengers = models.ManyToManyField(Passenger, related_name='user')
