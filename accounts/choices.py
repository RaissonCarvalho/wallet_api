from django.db.models import TextChoices

class RiskProfileChoices(TextChoices):
    CONSERVADOR = 'C', 'Conservador'
    MODERADO = 'M', 'Moderado'
    ARROJADO = 'A', 'Arrojado'