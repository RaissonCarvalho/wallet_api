from django.db.models import TextChoices

class OperationChoices(TextChoices):
    COMPRA = 'C', 'Compra'
    VENDA = 'V', 'Venda'