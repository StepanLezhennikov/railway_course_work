from datetime import timedelta
from django.db import connection
from django.db.models import Count, Q
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from .models import Station, Route
from route.forms import SearchForm


def index(request):
    form = SearchForm()
    return render(request, 'route/index.html', {'form': form})


def station_autocomplete(request):
    if 'term' in request.GET:
        search_term = request.GET.get('term')
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM route_station WHERE name ILIKE %s", [f'%{search_term}%'])
            stations = cursor.fetchall()
        station_names = [station[0] for station in stations]
        return JsonResponse(station_names, safe=False)
    return JsonResponse([], safe=False)


def search(request):

    start_time = timezone.datetime.fromisoformat(request.POST.get('travel_date'))
    end_time = start_time + timedelta(days=1)
    from_station = request.POST.get('from_station')
    to_station = request.POST.get('to_station')
    routes = Route.objects.filter(
        from_station__name=from_station,
        to_station__name=to_station,
        departure_time__gt=start_time,
        departure_time__lt=end_time
    ).select_related('train').annotate(
        free_seats=Count('train__cars__seats', filter=Q(train__cars__seats__is_occupied=False))
    )
    return render(request, 'route/result_search.html', context={'routes': routes})
