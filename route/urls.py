from django.urls import path

from route import views
from route.views import station_autocomplete, search

urlpatterns = [
    path('', views.index, name='home'),
    path('station-autocomplete/', station_autocomplete, name='station_autocomplete'),
    path('search', search, name='search')
]