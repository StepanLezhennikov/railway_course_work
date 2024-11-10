from datetime import datetime
from typing import List
from django.contrib import messages
from .tasks import send_ticket_email
from django.db import transaction
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from order.models import Order
from route.models import Route
from route.views import search
from train.models import Train


def finish_order(request):
    if request.method == "POST":
        selected_seats: List[dict] = request.session['selected_seats']
        route_id = request.session['route_id']
        route = Route.objects.prefetch_related('train__cars__seats').get(pk=route_id)

        selected_passengers_ids = [selected_id for selected_id in
                                   request.user.passengers.all().values_list('id', flat=True)
                                   if request.POST.get(f"selected_passengers_{selected_id}")]


        if len(selected_seats) != len(selected_passengers_ids):
            messages.error(request, "Количество пассажиров и мест не совпало")
            return redirect('passenger_add')

        seat_map = {(car.number, seat.number): seat for car in route.train.cars.all() for seat in car.seats.all()}

        with transaction.atomic():
            orders = []
            for passenger_id, seat_data in zip(selected_passengers_ids, selected_seats):
                seat_number, wagon_number = seat_data.values()
                seat = seat_map.get((int(wagon_number), int(seat_number)))

                if seat :
                    seat.is_occupied = True
                    seat.save()
                    orders.append(Order(
                        user=request.user,
                        passenger_id=passenger_id,
                        route=route,
                        seat=seat,
                        price=route.starting_price,
                        is_active=False
                    ))

        Order.objects.bulk_create(orders)
        user_orders = Order.objects.filter(user=request.user, is_active=False).select_related('route__train', "route__to_station")
        return render(request, "order/basket.html", context={"orders": user_orders})

    else:
        return redirect('passenger_add')


def basket(request):
    user_orders = Order.objects.filter(user=request.user, is_active=False).select_related('route__train',
                                                                                          "route__to_station")
    return render(request, "order/basket.html", context={"orders": user_orders})

def orders(request):
    user_orders = Order.objects.filter(user=request.user, is_active=True, route__arrival_time__gt=datetime.now()).select_related("route__train",
                                                                                          "route__to_station")
    return render(request, "order/orders.html", context={"orders": user_orders})



def return_ticket(request, order_id):
    order = Order.objects.get(pk=order_id)
    seat = order.seat
    seat.is_occupied = False
    seat.save()
    order.delete()

    next_page = request.GET.get('next', 'basket')
    return redirect(next_page)

def buy_tickets(request):
    orders = Order.objects.filter(user=request.user, is_active=False).select_related('route', 'passenger', 'seat__car')

    for order in orders:
        departure_time = order.route.departure_time.strftime('%d.%m.%Y %H:%M')
        arrival_time = order.route.arrival_time.strftime('%d.%m.%Y %H:%M')

        order_info = f"""
            Билет успешно куплен.
            {order.route}
            Время отправления: {departure_time}
            Время прибытия: {arrival_time}

            Пассажир: {order.passenger}
            Вагон: {order.seat.car.number}
            Место: {order.seat.number}
            """

        send_ticket_email.delay(request.user.email, order_info)
    orders.update(is_active=True)
    return redirect('home')
