from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .views import RegisterView, CustomLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('passengers/', views.passengers, name="passengers"),
    path('passenger_add/', views.add_passenger, name="passenger_add"),
    path('accounts/profile/', views.profile, name="profile"),
]
