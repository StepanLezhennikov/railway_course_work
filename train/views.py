from django.shortcuts import render

from train.models import Car, Train


def ticket_selection(request, route_id):
    train_id = Train.objects.get(id=route_id).id
    wagons = Car.objects.filter(train__pk=train_id).prefetch_related('seats')
    request.session['train_id'] = train_id
    request.session['route_id'] = route_id
    return render(request, 'train/ticket_selection.html', context={'wagons': wagons})
