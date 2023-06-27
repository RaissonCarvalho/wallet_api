from django.core.validators import MinValueValidator
from django.db.models import FloatField


class PositiveFloatField(FloatField):
    default_validators = [MinValueValidator(0.01, 'Valor tem que ser maior que zero')]
    null=False
    blank=False