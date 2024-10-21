from django.shortcuts import render


def discounts(request):
    return render(request, "discount/discounts.html")
