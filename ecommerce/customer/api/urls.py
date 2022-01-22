from django.urls import path
from customer.api import views

app_name = 'customer_api'

urlpatterns = [
  path('', views.create_customer_api_view, name='create_customer'),
  path('<str:id>', views.update_customer_api_view, name='update_customer')
]