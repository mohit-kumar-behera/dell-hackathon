# import Models
from customer.models import Customer
from product.models import Product

# import Serializers
from customer.api.serializers import CustomerSerializer
from product.api.serializers import ProductSerializer

MODEL_MAPPER = {
  'customer': Customer,
  'product': Product
}

SERIALIZER_MAPPER = {
  'customer': CustomerSerializer,
  'product': ProductSerializer
}