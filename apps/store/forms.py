from django import forms
from .models import Product, ShippingAdress

class ProductCreateForm(forms.ModelForm):
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

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAdress
        fields = [
            'address',
            'city',
            'state',
            'payment_method',
        ]