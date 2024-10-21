from django.shortcuts import render


def busket(request):
    return render(request, "order/busket.html")
