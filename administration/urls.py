from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.userManagement, name='userManagement'),
    path('user/delete/', views.user_delete, name='user_delete'),
    path('product/', views.productManagement, name='productManagement'),
    path('product/delete/', views.product_delete, name='product_delete'),
    path('product/expiryNotice/', views.product_expiry_notice, name='product_expiry_notice'),
    path('order/', views.orderManagement, name='orderManagement'),
    path('order/delete', views.order_delete, name='order_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/<int:nid>/profile/', views.edit_profile, name='edit_profile'),
    path('edit/<int:nid>/product/', views.edit_product, name='edit_product')
]
