from django.urls import path
from product.api import views

app_name = 'product_api'

urlpatterns = [
  path('', views.create_product_api_view, name='create_product'),
  path('/<str:id>', views.update_product_api_view, name='update_product')
]