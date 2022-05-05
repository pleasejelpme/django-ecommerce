from django.db import models
from products.models import Product
from django.contrib.auth.models import User

# Create your models here.

class ShoppingCart(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = 'ShoppingCart'
        verbose_name_plural = 'ShoppingCarts'

    def __str__(self):
        pass

