from django.urls import path
from . import views


urlpatterns = [
    path('transactions', views.TransactionList.as_view(), name='api-transaction-list'),
    path('transactions/<int:pk>', views.TransactionDetail.as_view(), name='api-transaction-detail'),
    path('transactions/stock/<int:pk>', views.TransactionStockList.as_view(), name='api-stock-transaction-list'),
    path('stocks/', views.StockList.as_view(), name='stock-list'),
    path('stocks/<int:pk>', views.StockDetail.as_view(), name='stock-detail'),

]