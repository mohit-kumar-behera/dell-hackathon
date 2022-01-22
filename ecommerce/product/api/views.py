from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from product.models import Product


@api_view(['POST'])
def create_product_api_view(request):
  if request.method == 'POST':
    return Response(data='product created', status=status.HTTP_201_CREATED)
  return Response(data = None, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def update_product_api_view(request, id):
  if request.method == 'POST':
    return Response(data=f'product id-{id} updated', status=status.HTTP_201_CREATED)
  return Response(data = None, status = status.HTTP_405_METHOD_NOT_ALLOWED)