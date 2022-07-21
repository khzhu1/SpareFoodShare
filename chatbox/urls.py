from django.urls import path,include
from . import views

# url for the chatbox app
urlpatterns = [
    path('', views.index, name="chatindex"),
    path('<str:username>/', views.chatPage, name="chatPage"),
]