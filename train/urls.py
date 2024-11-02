from django.contrib import admin
from django.urls import path

from train.views import ticket_selection

urlpatterns = [
    path('/<int:train_id>/', ticket_selection, name='ticket_selection')
]
