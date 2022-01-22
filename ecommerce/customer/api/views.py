from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth import get_user_model

from customer.models import Customer
from customer.api.serializers import CustomerSerializer

User = get_user_model()


@api_view(['POST'])
def create_customer_api_view(request):
  if request.method == 'POST':
    email = request.data.get('email', None)
    password = request.data.get('password', None)

    if not email or not password:
      return Response(data = 'Email and Password are compulsory fields', status = status.HTTP_400_BAD_REQUEST)

    # Create User
    try:
      user = User.objects.create_user(email=email, password=password)
    except:
      return Response(data = 'It seems account with this email already exists', status = status.HTTP_400_BAD_REQUEST)
    else:
      first_name = request.data.get('first_name', '')
      last_name = request.data.get('last_name', '') 
      
      user.first_name = first_name
      user.last_name = last_name
      user.save()
    
    if not user:
      return Response(data = 'Sorry, something went wrong while creating your account', status = status.HTTP_400_BAD_REQUEST)

    # Create Customer
    city = request.data.get('city', '')
    pin = request.data.get('pin', '')
    state = request.data.get('state', '')
    country = request.data.get('country', '')
    try:
      customer = Customer.objects.get(user = user)
    except Customer.DoesNotExist:
      return Response(data = 'Sorry, something went wrong while creating your account', status = status.HTTP_400_BAD_REQUEST)

    customer.city = city
    customer.pin = pin
    customer.state = state
    customer.country = country
    customer.save()

    serializer = CustomerSerializer(customer, many = False)  

    return Response(data = serializer.data, status = status.HTTP_201_CREATED)
  return Response(data = None, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def update_customer_api_view(request, id):
  if request.method == 'POST':
    return Response(data=f'customer id-{id} updated', status=status.HTTP_200_OK)
  return Response(data = None, status = status.HTTP_405_METHOD_NOT_ALLOWED)