from django.shortcuts import render

from train.models import Car


def ticket_selection(request, train_id):
    wagons = Car.objects.filter(train__pk=train_id).prefetch_related('seats')
    return render(request, 'train/ticket_selection.html', context={'wagons': wagons})
