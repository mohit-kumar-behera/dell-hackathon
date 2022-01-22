from django.db import models
from django.core.exceptions import ValidationError

import uuid

# creating a validator function
def positive_value(value):
    if value >= 0:
        return value
    else:
        raise ValidationError("Value should be positive")

class Product(models.Model):
  id = models.UUIDField(default = uuid.uuid4, primary_key = True, unique = True, editable = False)
  name = models.CharField(verbose_name ='Product Name', max_length = 255, blank = True, null = True)
  description = models.TextField(verbose_name ='Product Description', blank = True, null = True)
  quantity = models.IntegerField(verbose_name ='Quantity', default = 1, blank = True, null = True, validators = [positive_value])
  price = models.FloatField(verbose_name ='Price', default = 0, blank = True, null = True, validators = [positive_value])

  def __str__(self):
    return self.name
