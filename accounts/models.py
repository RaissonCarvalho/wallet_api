from django.db import models
from .choices import RiskProfileChoices
from django.contrib.auth.models import User


class Investor(models.Model):
  name = models.CharField(max_length=50, blank=False, null=False, default="")
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
  risk_profile = models.CharField(max_length=20, choices=RiskProfileChoices.choices, blank=False, null=False)

  def __str__(self) -> str:
    return f"{self.name} ({self.risk_profile})"
  