from rest_framework import serializers

from customer.models import Customer

from accounts.api.serializers import UserSerializer

class CustomerSerializer(serializers.ModelSerializer):
  user = UserSerializer(many=False)
  class Meta:
    model = Customer
    fields = '__all__'