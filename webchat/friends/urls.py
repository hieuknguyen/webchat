from django.urls import path
from . import views

urlpatterns = [
    path('get_friends/', views.get_friends, name='get_friends'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('accept_friend/', views.accept_friend, name='accept_friend'),
    
    
]
