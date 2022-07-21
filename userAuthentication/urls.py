from userAuthentication import views
from django.urls import path

urlpatterns = [
    path('login', views.login, name='loginUser'),
    path('login/<int:nid>', views.firstLogin, name='firstLogin'),
    path('register', views.register),
    path('profile', views.UserProfile, name='userProfile'),
    path('editfile/<int:nid>', views.EditProfile),
    path('edit/<int:nid>/account', views.EditProfile, name='editAccount')
]

