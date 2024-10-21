from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegistrationForm


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = 'users/login.html'


def passengers(request):
    return render(request, "users/passengers.html")
