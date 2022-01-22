from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from customer.models import Customer


@api_view(['POST'])
def create_customer_api_view(request):
  if request.method == 'POST':
    return Response(data='customer created', status=status.HTTP_201_CREATED)
  return Response(data = None, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def update_customer_api_view(request, id):
  if request.method == 'POST':
    return Response(data=f'customer id-{id} updated', status=status.HTTP_200_OK)
  return Response(data = None, status = status.HTTP_405_METHOD_NOT_ALLOWED)