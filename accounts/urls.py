from django.urls import path
from . import views


urlpatterns = [
    path('investors/', views.InvestorList.as_view(), name='investor-list'),
]