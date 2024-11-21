from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .views import RegisterView, CustomLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('passengers/', views.passengers, name="passengers"),
    path('delete_passenger/<int:passenger_id>', views.delete_passenger, name="delete_passenger"),
    path('passenger_add/', views.add_passenger, name="passenger_add"),
    path('passenger_create/', views.passenger_create, name="passenger_create"),
    path('accounts/profile/', views.profile, name="profile"),
]
