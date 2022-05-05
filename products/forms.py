from django.forms import ModelForm 
from .models import Product, Category

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'category',
            'description',
            'price',
            'stock')

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

