from rest_framework import serializers
from .models import Investor
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
  class Meta:
     model = User
     fields = [
        'username',
        'email',
        'password',
     ]


class InvestorSerializer(serializers.ModelSerializer):
   user = UserSerializer()

   class Meta:
      model = Investor
      fields = [
         'id',
         'name',
         'risk_profile',
         'user',
      ]
   
   
   def create(self, validated_data):
      user_data = validated_data.pop('user')
      user = User.objects.create_user(
         username=user_data['username'],
         email=user_data['email'],
         password=user_data['password'],
      )

      return Investor.objects.create(user=user, **validated_data)