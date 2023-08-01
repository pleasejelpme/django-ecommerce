from django import forms
from .models import Product, Checkout

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

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = [
            'address',
            'city',
            'state',
            'payment_method',
            'transfer_reference',
        ]
        
        labels = {
            'address': ('Address'),
            'city': ('City'),
            'state': ('State'),
            'transfer_reference': ('Transfer reference (only if your paying with bank transfer!)'),
            'payment_method': ('Payment method')
        }