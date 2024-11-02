from django.urls import path
from discount.views import discounts

urlpatterns = [
    path('discounts/', discounts, name="discounts"),
]
