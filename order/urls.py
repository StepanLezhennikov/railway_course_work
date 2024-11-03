from django.urls import path
from order.views import basket, finish_order, return_ticket, buy_tickets, orders

urlpatterns = [
    path('basket/', basket, name="basket"),
    path('orders/', orders, name="orders"),
    path('finish_order/', finish_order, name="finish_order"),
    path('return_ticket/<int:order_id>', return_ticket, name="return_ticket"),
    path('buy_tickets/', buy_tickets, name="buy_tickets"),
]
