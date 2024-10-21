from django.urls import path
from order.views import busket

urlpatterns = [
    path('busket/', busket, name="busket"),
]
