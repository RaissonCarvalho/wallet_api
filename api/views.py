from api.models import Stock, Transaction
from accounts.models import Investor

from .serializers import StockSerializer, TransactionGetSerializer, TransactionPostSerializer, TransactionUpdateSerializer
from .utils import get_dates_obj, calculate_average_price

from .permissions import IsInvestorOwner
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError


class TransactionList(generics.ListCreateAPIView):
  permission_classes = [IsAuthenticated, IsInvestorOwner]
  

  def get_serializer_class(self):
    """
      Caso método HTTP seja GET retorna TransactionGetSerializer.
      Caso método HTTP seja POST retorna TransactionPostSerializer.
    """
    if self.request.method == 'GET':
      return TransactionGetSerializer
    else:
      return TransactionPostSerializer 

  """
    Se houver parâmetros inital-date e  end-date na URL
    queryset é definido atráves do filtro desses parâmetros,
    caso contrário queryset retorna todas as transações do
    Investor autenticado.
  """
  def get_queryset(self):
    user = self.request.user
    investor = Investor.objects.get(user=user)
    if 'inital-date' in self.request.GET and 'end-date' in self.request.GET:
      try:
        dates = get_dates_obj(self.request.GET['inital-date'], self.request.GET['end-date'], self.request)
        inital_date = dates['inital_date']
        end_date = dates['end_date']

        queryset = Transaction.objects.filter(date__range=[inital_date, end_date], investor=investor).order_by('date')
      except ValueError:
        raise ValidationError(
          detail={
            "message": "Date params does not match format '%Y-%m-%d' ",
            "status": status.HTTP_400_BAD_REQUEST,
          },
        )

      if queryset:
        return queryset
      else:
        raise NotFound(
          detail={
            "message": "Stock not found",
            "status_code": status.HTTP_404_NOT_FOUND,
          },
        )
    
    return Transaction.objects.filter(investor=investor).order_by('date')

  def get(self, request, *args, **kwargs):
    transactions = self.get_queryset()
    serializer = self.get_serializer(transactions, many=True)
    return Response(
         {
            "message": "Transactions Retrieved Successfully.",
            "status": status.HTTP_200_OK,
            "transactions": serializer.data,
            "result_count": transactions.count(),
         },
         status=status.HTTP_200_OK
      )
  
  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(
        {
          "message": "New Registred Transaction.",
          "status": status.HTTP_201_CREATED,
          "stock": serializer.data,
        },
        status=status.HTTP_201_CREATED
      )
    else:
      return Response(
        {
          "status": status.HTTP_400_BAD_REQUEST,
          "error": serializer.error
        },
        status=status.HTTP_400_BAD_REQUEST
      ) 


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = TransactionGetSerializer
  queryset = Transaction.objects.all()
  permission_classes = [IsAuthenticated, IsInvestorOwner]

  def get(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return Response(
         {
            "message": "Transaction '{}' Retrieved Successfully.".format(instance),
            "status": status.HTTP_200_OK,
            "transaction": serializer.data,
         },
         status=status.HTTP_200_OK
    )
  
  def put(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = TransactionUpdateSerializer(instance=instance, data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(
        {
          "message": "Transaction '{}' Updated Successfully.".format(instance),
          "status": status.HTTP_200_OK,
          "transaction": serializer.data,
        },
        status=status.HTTP_200_OK
      )
    else:
      return Response(
        {
          "status": status.HTTP_400_BAD_REQUEST,
          "error": serializer.errors
        }
      )
  
  def patch(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = TransactionUpdateSerializer(instance=instance, data=request.data, partial=True)

    if serializer.is_valid():
      serializer.save()
      return Response(
        {
          "message": "Transaction '{}' Updated Successfully.".format(instance),
          "status": status.HTTP_200_OK,
          "transaction": serializer.data,
        },
        status=status.HTTP_200_OK
      )
    else:
      return Response(
        {
          "status": status.HTTP_400_BAD_REQUEST,
          "error": serializer.errors
        }
      ) 
  
  def delete(self, request, *args, **kwargs):
    self.destroy(request, *args, **kwargs)

    return Response(
      {
        "message": "Transaction Deleted Successfully.",
        "status": status.HTTP_204_NO_CONTENT,
      },
      status=status.HTTP_204_NO_CONTENT
    )


class TransactionStockList(generics.ListAPIView):
  serializer_class = TransactionGetSerializer
  permission_classes = [IsAuthenticated, IsInvestorOwner]

  def get_queryset(self):
    
    user = self.request.user
    investor = Investor.objects.get(user=user)
    try:
      stock = Stock.objects.get(id=self.kwargs['pk'])
    except Stock.DoesNotExist:
      raise NotFound(
        detail={
          "message": "Transaction for this Stock doesn't exist",
          "status_code": status.HTTP_404_NOT_FOUND,
        }
                
      )

    queryset = Transaction.objects.filter(stock=stock, investor=investor).order_by('date')

    return queryset
  
  def get(self, request, **kwargs):
    transactions = self.get_queryset()
    serializer = self.get_serializer(transactions, many=True)

    stock = stock = Stock.objects.get(id=self.kwargs['pk'])

    if transactions:
      average_price = calculate_average_price(transactions)        
        
      return Response(
        {
          "message": "{} stock transactions successfully retrieved.".format(stock.code),
          "status": status.HTTP_200_OK,
          "transactions": serializer.data,
          "average_price": average_price,
          "result_count": transactions.count(),
        },
        status=status.HTTP_200_OK
      )
    else:
      return Response(
        {
          "message": "There's no transactions for this stock",
          "status": status.HTTP_404_NOT_FOUND,
        },
        status=status.HTTP_404_NOT_FOUND
      )


class StockList(generics.ListCreateAPIView):
  serializer_class = StockSerializer
  queryset = Stock.objects.all()
  permission_classes = [IsAuthenticated,]

  def get(self, request, *args, **kwargs):
    stocks = self.get_queryset()
    serializer = self.get_serializer(stocks, many=True)
    return Response(
         {
            "message": "Stocks Retrieved Successfully.",
            "status": status.HTTP_200_OK,
            "stocks": serializer.data,
            "result_count": stocks.count(),
         },
         status=status.HTTP_200_OK
    )
   
  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(
          {
            "message": "New Registred Stock. ",
            "status": status.HTTP_201_CREATED,
            "stock": serializer.data,
          },
          status=status.HTTP_201_CREATED
      )
    else:
      return Response(
        {
          "status": status.HTTP_400_BAD_REQUEST,
          "error": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
      )


class StockDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = StockSerializer
  queryset = Stock.objects.all()
  permission_classes = [IsAuthenticated,]

  def get(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return Response(
         {
            "message": "Stock '{}' Retrieved Successfully.".format(instance),
            "status": status.HTTP_200_OK,
            "stock": serializer.data,
         },
         status=status.HTTP_200_OK
    )