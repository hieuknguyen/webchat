from django.urls import path
from . import views

urlpatterns = [
    path('add_friend/', views.add_friend, name='add_friend'),
]
