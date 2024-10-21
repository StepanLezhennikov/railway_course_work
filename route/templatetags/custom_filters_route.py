from django import template
import datetime

register = template.Library()


@register.filter(name='duration')
def duration(value, arg):
    if isinstance(value, datetime.datetime) and isinstance(arg, datetime.datetime):
        delta = arg - value
        hours, remainder = divmod(delta.seconds, 3600)
        minutes = remainder // 60

        if minutes and hours:
            return f'{hours}ч {minutes}мин'
        if hours:
            return f'{hours}ч'
        if minutes:
            return f'{minutes}мин'
    return ''
