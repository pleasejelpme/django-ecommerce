from django.forms import ModelForm
from .models import Product

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