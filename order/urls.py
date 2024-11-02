from django.urls import path
from order.views import basket, finish_order

urlpatterns = [
    path('basket/', basket, name="basket"),
    path('finish_order/', finish_order, name="finish_order"),
]
