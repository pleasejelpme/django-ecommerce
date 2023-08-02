from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    document_id = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_customer(instance, created, *args, **kwargs):
    if created:
        Customer.objects.create(user=instance)
