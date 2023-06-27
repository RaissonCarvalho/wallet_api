from .models import Investor

from .serializers import InvestorSerializer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


class InvestorList(generics.ListCreateAPIView):
  queryset = Investor.objects.all()
  serializer_class = InvestorSerializer


  def get(self, request, *args, **kwargs):
    investors = self.get_queryset()
    serializer = self.get_serializer(investors, many=True)

    return Response(
      {
        "message": "Investors Retrieved Successfully.",
        "status": status.HTTP_200_OK,
        "investors": serializer.data,
        "result_count": investors.count(),
      },
      status=status.HTTP_200_OK
    )


  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
      serializer.save()
      return Response(
        {
          "message": "New registered investor",
          "status": status.HTTP_201_CREATED,
          "investor": serializer.data,
        },
        status=status.HTTP_201_CREATED
      )
