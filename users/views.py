from datetime import datetime

from django.contrib.auth.views import LoginView
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
    return render(request, "users/passengers.html")


@login_required(login_url="login")
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=request.user, is_active=True,
                                       route__arrival_time__gt=datetime.now()).select_related("route__train",
                                                                                              "route__to_station")
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

        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        fathername = request.POST.get('fathername')
        passport_number = request.POST.get('passport_number')
        is_child = request.POST.get('is_child') == "on"

        passenger = Passenger.objects.create(
            first_name=first_name,
            second_name=second_name,
            fathername=fathername,
            passport_number=passport_number,
            is_child=is_child
        )

        request.user.passengers.add(passenger)
        selected_passengers = request.session.get('selected_passengers', [])
        selected_passengers.append(passenger.id)
        request.session['selected_passengers'] = selected_passengers

        return redirect(reverse('passenger_add'))

    if request.POST.get('selected_seats', '[]'):
        selected_seats = json.loads(request.POST.get('selected_seats', '[]'))
        request.session['selected_seats'] = selected_seats
    else:
        messages.error(request, "Не выбраны места.")
        redirect('ticket_selection')

    return render(request, 'users/passenger_add.html', {'user': request.user})
