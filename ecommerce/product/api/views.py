from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from product.models import Product
from product.api.serializers import ProductSerializer


@api_view(['POST'])
def create_product_api_view(request):
  if request.method == 'POST':
    serializer = ProductSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(data = serializer.data, status = status.HTTP_201_CREATED)
    return Response(data='product not created', status=status.HTTP_400_BAD_REQUEST)
  return Response(data = None, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def update_product_api_view(request, id):
  if request.method == 'POST':
    try:
      product = Product.objects.get(id = id)
    except Product.DoesNotExist:
      return Response(data = 'Product with this ID doesnot exists', status = status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product, data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(data = serializer.data, status = status.HTTP_200_OK)
    return Response(data = 'Sorry the product couldnot be updated, Please verify the fields and submit again', status=status.HTTP_400_BAD_REQUEST)
  return Response(data = None, status = status.HTTP_405_METHOD_NOT_ALLOWED)