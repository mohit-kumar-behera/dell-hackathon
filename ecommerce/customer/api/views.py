from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.conf import settings

from customer.models import Customer
from customer.api.serializers import CustomerSerializer

User = get_user_model()
tracker = settings.AUDIT_TRACKER


@api_view(['POST'])
def create_customer_api_view(request):
  if request.method == 'POST':

    if not request.data.get('email', None) or not request.data.get('password', None):
      return Response(data = 'Email and password field cant be empty', status=status.HTTP_400_BAD_REQUEST) 
    
    request.data['password'] = make_password(request.data.get('password'))

    serializer = CustomerSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(data = serializer.data, status = status.HTTP_201_CREATED)
    
    return Response(data='customer not created', status=status.HTTP_400_BAD_REQUEST)
  return Response(data = None, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def update_customer_api_view(request, id):
  if request.method == 'POST':
    try:
      customer = Customer.objects.get(id = id)
    except Customer.DoesNotExist:
      return Response(data = 'Customer with this ID doesnot exists', status = status.HTTP_404_NOT_FOUND)
    
    old_serializer = CustomerSerializer(customer)
    old_data = old_serializer.data
    new_data = request.data
    table_name = customer.__class__.__name__.lower()

    serializer = CustomerSerializer(customer, data = new_data)
    if serializer.is_valid():
      serializer.save()
      # Add tracker
      tracker.add_to_tracker(table_name, 'id', old_data, new_data)
      return Response(data = serializer.data, status = status.HTTP_200_OK)

    return Response(data = 'Update not done', status = status.HTTP_400_BAD_REQUEST)
  return Response(data = None, status = status.HTTP_405_METHOD_NOT_ALLOWED)
