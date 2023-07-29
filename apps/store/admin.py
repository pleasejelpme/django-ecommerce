from django.contrib import admin
from .models import Category, Product, Order, ProductOrder, ShippingAdress

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ProductOrder)
admin.site.register(ShippingAdress)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'tag_list', 'stock', 'price']

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

