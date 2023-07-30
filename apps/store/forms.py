from django.forms import ModelForm
from .models import Product, ShippingAdress

class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'tags',
            'price',
            'description',
            'stock'
        ]

class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAdress
        fields = [
            'address',
            'city',
            'state',
            'payment_method'
        ]