from django.urls import path
from discount.views import discounts, buy_discount_card, choose_discounts

urlpatterns = [
    path('discounts/', discounts, name="discounts"),
    path('choose_discounts/', choose_discounts, name="choose_discounts"),
    path('buy_discount_card/<int:card_id>', buy_discount_card, name="buy_discount_card"),
]
