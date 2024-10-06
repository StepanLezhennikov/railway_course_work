from django import template

register = template.Library()

@register.filter
def free_seats_count(car):
    count = car.seats.filter(is_occupied=False).count()
    return count