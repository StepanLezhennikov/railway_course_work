from django.core.exceptions import ValidationError


def validate_first_letter_uppercase(value):
    if not value[0].isupper():
        raise ValidationError('Первая буква должна быть заглавной.')
