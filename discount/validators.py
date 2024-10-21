from django.core.exceptions import ValidationError


def between_0_and_1(value):
    if not 0 <= value <= 1:
        raise ValidationError('Значение должно быть между 0 и 1')
