from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.conf import settings

from data_audit.api.model_mapper import MODEL_MAPPER, SERIALIZER_MAPPER

tracker = settings.AUDIT_TRACKER


@api_view(['GET'])
def fetch_delta_change_api_view(request, model):
  Model = MODEL_MAPPER.get(model, None)
  ModelSerializer = SERIALIZER_MAPPER.get(model, None)
  
  if not Model or not ModelSerializer:
    return Response(data = 'Specified Model is not found', status = status.HTTP_404_NOT_FOUND)
  
  current_snapshot = Model.objects.all()
  serializer = ModelSerializer(current_snapshot, many = True)

  data = tracker.track_delta(serializer.data, model, 'id')

  if data:
    return Response(data = data, status = status.HTTP_200_OK)
  return Response(data = 'Unable to fetch data audit', status = status.HTTP_404_NOT_FOUND)
