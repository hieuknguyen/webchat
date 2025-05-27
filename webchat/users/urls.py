from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_form, name='register_form'),
    path('login/', views.login_form, name='login_form'),
]
