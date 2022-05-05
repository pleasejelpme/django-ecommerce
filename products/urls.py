from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('product/<int:id>/', views.product_detail_view, name='product-detail'),
    path('product/add/', views.create_product_view, name='product-create'),
    path('product/list/', views.product_list_view, name='product-list'),
    path('category/add/', views.create_category_view, name='category-create'),
    path('product/update/<int:id>', views.update_product_view, name='product-update'),
    path('product/delete/<int:id>', views.delete_view, name='product-delete'),
]