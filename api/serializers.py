from rest_framework import serializers, exceptions, status
from .models import Transaction, Stock
from accounts.models import Investor


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = [
            'id',
            'code',
            'company_name',
            'cnpj',
        ]


class TransactionGetSerializer(serializers.ModelSerializer):
    stock_code = serializers.CharField(source='stock.code')

    total_trading_amount = serializers.SerializerMethodField('total_value')
    def total_value(self, transaction):
        return transaction.get_total_trading_amount()

    
    class Meta:
        model = Transaction
        fields = [
            'id',
            'date',
            'stock_code',
            'operation_type',
            'quantity',
            'unit_price',
            'brokerage',
            'total_trading_amount',
        ]
    
    
class TransactionPostSerializer(serializers.ModelSerializer):
    stock_code = serializers.CharField(source='stock.code')

    class Meta:
        model = Transaction
        fields = [
            'id',
            'date',
            'stock_code',
            'operation_type',
            'quantity',
            'unit_price',
            'brokerage',
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        investor = Investor.objects.get(user=user)
        stock_code = validated_data.pop('stock')['code']

        try:
            stock = Stock.objects.get(code=stock_code)
        except Stock.DoesNotExist:
            raise exceptions.NotFound(
                detail={
                    "message": "Stock not found",
                    "status_code": status.HTTP_404_NOT_FOUND,
                }
                
            )
        return Transaction.objects.create(investor=investor, stock=stock ,**validated_data)
    

class TransactionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = [
            'id',
            'date',
            'operation_type',
            'quantity',
            'unit_price',
            'brokerage',
        ]
    
    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)

        instance.operation_type = validated_data.get('operation_type', instance.operation_type)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.brokerage = validated_data.get('brokerage', instance.brokerage)

        instance.save()

        return instance
    
    