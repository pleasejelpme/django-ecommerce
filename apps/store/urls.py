from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/add', views.product_create, name='product-create'),
    path('product/<str:pk>', views.product_detail, name='product-detail'),
    path('cart/', views.shopping_cart, name='cart'),
    path('categories/', views.category_list, name='categories'),
    path('checkout/<str:pk>', views.checkout, name='checkout'),
]
