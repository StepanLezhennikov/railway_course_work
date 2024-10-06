from django.shortcuts import render


def ticket_selection(request):
    return render(request, 'train/ticket_selection.html')
