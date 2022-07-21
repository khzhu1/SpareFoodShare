from homePage import views
from django.urls import path

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('<int:nid>', views.homePageWithFilter, name='homePageWithFilter'),
    path('logout', views.logout, name='logoutUser'),
    path('addItem', views.addItem, name='addItem'),
    path('viewItem', views.viewItem, name='viewItem'),
    path('myList', views.myList, name='myList'),
    path('map', views.map, name='map'),
    path('search/<str:keyword>/result', views.searchHomePage, name='searchHomePage'),
    path('viewMyItem', views.viewMyItem, name='viewMyItem'),
    path('changeVisibility', views.changeVisibility, name='changeVisibility'),
    path('maddItem', views.maddItem, name='maddItem'),

]
