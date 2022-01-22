from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from customer.models import Customer
User = get_user_model() 

"""Create Profile when User is created"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Customer.objects.create(user=instance)
        except:
            pass


"""Update Profile when User is updated"""
@receiver(post_save, sender=User)
def update__user_profile(sender, instance, created, **kwargs):
    if not created and instance.customer:
        instance.customer.save()


"""Delete the user when Profile of that User is deleted"""
@receiver(post_delete, sender=Customer)
def delete_user(sender, instance, **kwargs):
    instance.user and instance.user.delete()