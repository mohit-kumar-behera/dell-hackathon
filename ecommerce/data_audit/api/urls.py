from django.urls import path
from data_audit.api import views

app_name = 'data_audit_api'

urlpatterns = [
  path('<str:model>', views.fetch_delta_change_api_view, name = 'fetch_delta_change')
]