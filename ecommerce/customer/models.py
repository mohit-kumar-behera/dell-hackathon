from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

import uuid

User = get_user_model()

class Customer(models.Model):
  id = models.UUIDField(default = uuid.uuid4, primary_key = True, unique = True, editable = False)
  first_name = models.CharField(verbose_name = 'First Name', max_length = 40, blank = True, null = True)
  last_name = models.CharField(verbose_name = 'Last Name', max_length = 40, blank = True, null = True)
  email = models.EmailField(verbose_name='Email Address', max_length=120, unique=True, blank = True, null = True)
  password = models.CharField(verbose_name='Password', max_length=255, blank = True, null = True)
  city = models.CharField(verbose_name = 'City', max_length = 100, blank = True, null = True)
  pin = models.CharField(verbose_name = 'PIN Code', max_length = 6, blank = True, null = True)
  state = models.CharField(verbose_name = 'State', max_length = 100, blank = True, null = True)
  country = models.CharField(verbose_name = 'Country', max_length = 100, blank = True, null = True)
  date_joined = models.DateTimeField(verbose_name = 'Date Joined', auto_now_add = True, blank = True, null = True)
  updated_at = models.DateTimeField(verbose_name = 'Updated Account at', auto_now = True, blank = True, null = True)

  def __str__(self):
    return self.email
  
  def save(self, *args, **kwargs):
    if self.state:
      self.state = self.state.capitalize()
    if self.country:
      self.country = self.country.capitalize()
    super(Customer, self).save(*args, **kwargs)

  def get_address(self):
    return f"{self.city}, Pin-{self.pin}, {self.state}, {self.country}"
  
  def get_fullname(self):
    return f'{self.first_name if self.first_name else ""} {self.last_name if self.last_name else ""}'



# @receiver(pre_save, sender = Customer)
# def handle_pre_save(sender, instance, *args, **kwargs):
#   print("PRE SAVE", instance.city)


# @receiver(post_save, sender = Customer)
# def handle_post_save(sender, instance, created, *args, **kwargs):
#   if created:
#     pass
#   else:
#     print("Not Created POST SAVE", instance.city)


"""
1) Created a new Customer
PRE SAVE mihir2@mail.com
Create POST SAVE mihir2@mail.com

2) Update existing customer
PRE SAVE mihir2@mail.com
Not Created POST SAVE mihir2@mail.com

"""