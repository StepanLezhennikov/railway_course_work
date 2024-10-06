from django.contrib import admin
from django.urls import path

from train.views import ticket_selection

urlpatterns = [
    path('', ticket_selection, name='ticket_selection')
]
