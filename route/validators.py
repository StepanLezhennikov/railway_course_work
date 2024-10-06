from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_first_letter_uppercase(value):
    if not value[0].isupper():
        raise ValidationError('Первая буква должна быть заглавной.')


def validate_date_more_than_now(date):
    if date <= timezone.now():
        raise ValidationError('Время должно быть больше текущего')
