from django import template

register = template.Library()

@register.filter
def multiply_by_100(value):
    try:
        return int(float(value) * 100)
    except (ValueError, TypeError):
        return value
