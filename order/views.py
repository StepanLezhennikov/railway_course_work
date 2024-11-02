from typing import List
from django.contrib import messages

from django.db import transaction
from django.shortcuts import render, redirect
import json

from train.models import Train


def finish_order(request):
    if request.method == "POST":
        selected_seats: List[dict] = request.session['selected_seats']
        train_id = request.session['train_id']
        train = Train.objects.prefetch_related('cars__seats').get(pk=train_id)

        selected_passengers_ids = [selected_id for selected_id in
                                   request.user.passengers.all().values_list('id', flat=True)
                                   if request.POST.get(f"selected_passengers_{selected_id}")]

        if len(selected_seats) != len(selected_passengers_ids):
            messages.error(request, "Количество пассажиров и мест не совпало")
            return redirect('passenger_add')

        seat_map = {(car.number, seat.number): seat for car in train.cars.all() for seat in car.seats.all()}

        with transaction.atomic():
            for seat_dict in selected_seats:
                seat_number, wagon_number = seat_dict.values()
                seat = seat_map.get((int(wagon_number), int(seat_number)))
                if seat:
                    seat.is_occupied = True
                    seat.save()

        return redirect('basket')


def basket(request):
    return render(request, "order/basket.html")
