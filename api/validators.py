import re
from pycpfcnpj import cpfcnpj
from django.core.exceptions import ValidationError

def validate_stock_code(value):
    pattern = r'^[A-Z]{4}[0-9]{1,2}$'
    if len(value) < 5 or not re.match(pattern, value):
        raise ValidationError('O código deve ter 5 ou 6 caracteres, com os 4 primeiros sendo letras maiúsculas e os 5º e 6º caracteres sendo números.')
    

def validate_cnpj(value):
    pattern = r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$'
    if cpfcnpj.validate(value) == False:
        raise ValidationError(
            'CNPJ inválido, tente novamente!'
        )
    if not re.match(pattern, value):
        raise ValidationError(
            'CNPJ inválido, tente novamente!'
        )