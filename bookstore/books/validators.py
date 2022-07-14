from django.core.exceptions import ValidationError
from .models import Author


def valid_email(val):  # валидация добавлена в модель данных
    if '.cmo' in val:
        raise ValidationError(".com (not '.cmo')")

    # проверка на существование почты в базе
    get_mail = Author.objects.filter(email=val)
    if get_mail:
        raise ValidationError("указанная почта использована ранее")



LAST_NAME = ['TIGER', 'CAT', 'PYTHON']


def validate_last_name(val):  # валидация добавлена в форму
    if val.upper() in LAST_NAME:
        err = f'{val} is not allowed as last name'
        raise ValidationError(err)
