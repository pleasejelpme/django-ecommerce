from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),    
    path('product/add', views.product_create, name='product-create'),
    path('product/<str:pk>', views.product_detail, name='product-detail'),
    path('cart/>', views.shopping_cart, name='shopping-cart'),
    path('update_cart/>', views.update_shopping_cart, name='update-cart'), 

]