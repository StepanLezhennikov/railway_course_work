from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from discount.models import DiscountCard, DiscountCardType
from train.models import TrainType


def discounts(request):
    # return render(request, "discount/discounts.html")
    user_cards = request.user.discounts.all()
    return render(request, "discount/discounts.html", context={'user_cards': user_cards, 'available_cards': DiscountCardType.objects.filter(is_active=True)})


def choose_discounts(request):
    selected_passengers_ids = [selected_id for selected_id in
                               request.user.passengers.all().values_list('id', flat=True)
                               if request.POST.get(f"selected_passengers_{selected_id}")]

    request.session['selected_passengers_ids'] = selected_passengers_ids

    user_cards = request.user.discounts.filter(amount_of_rides__gt=0, end_date__gt=datetime.now())
    if user_cards.exists():
        return render(request, "discount/choose_discount.html", context={'user_cards': user_cards})
    else:
        return redirect('finish_order')

def buy_discount_card(request, card_id):
    type_of_discount = DiscountCardType.objects.get(pk=card_id)
    if request.user.discounts.filter(type=type_of_discount).exists():
        messages.error(request, f"У вас уже есть такая карта.")
    else :
        new_card = DiscountCard.objects.create(type=type_of_discount, user=request.user)
    return redirect('discounts')

def delete_discount_card(request, card_id):
    # Логика удаления карты
    pass