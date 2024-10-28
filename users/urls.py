from django.urls import path

from . import views
from .views import RegisterView, CustomLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('passengers/', views.passengers, name="passengers"),
    path('accounts/profile/', views.profile, name="profile"),
]
