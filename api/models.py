from django.db import models
from .fields import PositiveFloatField
from .choices import OperationChoices
from accounts.models import Investor
from .validators import validate_stock_code, validate_cnpj


class Stock(models.Model):
    code = models.CharField(max_length=6, unique=True, blank=False, null=False, validators=[validate_stock_code])
    company_name = models.CharField(max_length=255, blank=False, null=False)
    cnpj = models.CharField(max_length=18, blank=False, null=False, unique=True ,validators=[validate_cnpj])

    def __str__(self):
        return f"{self.code} - {self.company_name} ({self.cnpj})"
    

class Transaction(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='transaction')
    operation_type = models.CharField(max_length=1, choices=OperationChoices.choices)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    unit_price = PositiveFloatField()
    brokerage = PositiveFloatField()
    date = models.DateField(null=False)

    def __str__(self):
        return f"{self.investor.name} - {self.stock.code} ({self.operation_type}) - {self.quantity} - {self.unit_price} - {self.date}"
    
    
    def get_total_trading_amount(self):
        if self.operation_type == 'C':
            total_value = (self.quantity * self.unit_price) + (self.brokerage+0.05)
            return round(abs(total_value), 2)
        if self.operation_type == 'V':
            total_value = (self.quantity * self.unit_price) - (self.brokerage+0.05)
            return round(abs(total_value), 2)