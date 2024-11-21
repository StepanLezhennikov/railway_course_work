from datetime import datetime

from django.contrib.auth.views import LoginView, LogoutView
from django.db import connection
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json

from order.models import Order
from users.forms import RegistrationForm
from users.models import Passenger


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')


def passengers(request):
    return render(request, "users/passengers.html", context={'passengers': request.user.passengers.all()})

def delete_passenger(request, passenger_id):
    # passenger = Passenger.objects.get(pk=passenger_id).delete()
    with connection.cursor() as cursor:
        cursor.execute("""
                                DELETE FROM users_user_passengers
                                WHERE passenger_id = %s AND user_id = %s   
                                """, [passenger_id, request.user.id])
        cursor.execute("""
                        DELETE FROM users_passenger
                        WHERE id = %s   
                        """, [passenger_id])
    return redirect('passengers')


@login_required(login_url="login")
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=request.user, is_active=True,
                                       route__arrival_time__gt=datetime.now()).select_related("route__train",
                                                                                              "route__to_station", "route__from_station")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT  
                   route_route.departure_time, 
                   route_route.arrival_time, 
                   to_st.name AS to_station_name,
                   fr_st.name AS from_station_name
            FROM order_order
            INNER JOIN route_route ON order_order.route_id = route_route.id
            INNER JOIN train_train ON route_route.train_id = train_train.id
            INNER JOIN route_station AS to_st ON route_route.to_station_id = to_st.id
            INNER JOIN route_station AS fr_st ON route_route.from_station_id = fr_st.id
            WHERE order_order.user_id = %s 
              AND order_order.is_active = TRUE
              AND route_route.arrival_time > %s
        """, [user.id, datetime.now()])
        columns = [col[0] for col in cursor.description]
        orders = [dict(zip(columns, row)) for row in cursor.fetchall()]



    discount_cards = user.discounts.all()
    passengers_all = user.passengers.all()

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        user.phone_number = phone_number
        user.save()
        messages.success(request, 'Номер телефона успешно добавлен.')
        return redirect('profile')

    context = {
        'user': user,
        'orders': orders,
        'discount_cards': discount_cards,
        'passengers': passengers_all
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url="login")
def add_passenger(request):
    if request.method == "POST" and request.POST.get('first_name'):
        if request.POST.get('selected_seats', '[]'):
            selected_seats = json.loads(request.POST.get('selected_seats', '[]'))
            request.session['selected_seats'] = selected_seats

        passenger = create_passenger(request)


        selected_passengers = request.session.get('selected_passengers', [])
        selected_passengers.append(passenger.id)
        request.session['selected_passengers'] = selected_passengers

        return redirect('passenger_add')

    if request.POST.get('selected_seats', '[]'):
        selected_seats = json.loads(request.POST.get('selected_seats', '[]'))
        request.session['selected_seats'] = selected_seats
    else:
        messages.error(request, "Не выбраны места.")
        redirect('ticket_selection')

    return render(request, 'users/passenger_add.html', {'user': request.user})


def create_passenger(request):
    first_name = request.POST.get('first_name')
    second_name = request.POST.get('second_name')
    fathername = request.POST.get('fathername')
    passport_number = request.POST.get('passport_number')
    is_child = request.POST.get('is_child') == "on"

    passenger = Passenger.objects.create(first_name=first_name,
            second_name=second_name,
            fathername=fathername,
            passport_number=passport_number,
            is_child=is_child)

    request.user.passengers.add(passenger)

    return passenger

def passenger_create(request):
    passenger = create_passenger(request)
    return redirect('passengers')