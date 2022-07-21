from django.urls import path
from . import views
from payment.views import *

urlpatterns = [
    path('pay/<str:id>/', views.CreatePayment, name='payment'),
    path('webhook/', views.stripe_webhook),
    path('add/', views.add, name='add'),
    path('order/', views.order, name= 'order'),
    path('success/', views.success, name= 'success'),
    path('refund/', views.Refund, name= 'refund'),
]