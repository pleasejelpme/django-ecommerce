from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('profile/', views.profile_page, name='profile-page'),
    path('profile-update/', views.edit_customer_info, name='profile-update'),
]
