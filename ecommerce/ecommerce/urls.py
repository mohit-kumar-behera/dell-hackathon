from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/customer/', include('customer.api.urls')),
    path('api/product/', include('product.api.urls')),
]
