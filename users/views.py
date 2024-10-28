from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.forms import RegistrationForm


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
    orders = user.orders.all()
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
