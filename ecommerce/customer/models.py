from django.db import models
from django.contrib.auth import get_user_model

import uuid

User = get_user_model()

class Customer(models.Model):
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  city = models.CharField(verbose_name='City', max_length=100, blank=True, null=True)
  pin = models.CharField(verbose_name='PIN Code', max_length=6, blank=True, null=True)
  state = models.CharField(verbose_name='State', max_length=100, blank=True, null=True)
  country = models.CharField(verbose_name='Country', max_length=100, blank=True, null=True)

  def __str__(self):
    return self.user.email
  
  def save(self, *args, **kwargs):
    if self.state:
      self.state = self.state.capitalize()
    if self.country:
      self.country = self.country.capitalize()
    super(Customer, self).save(*args, **kwargs)

  def get_address(self):
    return f"{self.city}, Pin-{self.pin}, {self.state}, {self.country}"
