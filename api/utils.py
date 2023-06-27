from datetime import datetime


def get_dates_obj(inital_date, end_date, request):
  dates = []
  inital_date_str = request.GET.get('inital-date')
  end_date_str = request.GET.get('end-date')
       
  inital_date = datetime.strptime(inital_date_str, '%Y-%m-%d').date()
  end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

  dates = {'inital_date': inital_date, 'end_date': end_date}
    
  return dates

def calculate_average_price(transactions):
  cont = 0
  average_price = 0

  for transaction in transactions:
    if transaction.operation_type == 'C':
      quantity = transaction.quantity
      total_trading_amount = transaction.get_total_trading_amount()
      average_price = ((cont * average_price) + total_trading_amount) / (cont + quantity)
      cont += quantity      
      
    
  return round(average_price, 2)
