from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_form, name='register'),
    path('login/', views.login_form, name='login'),
    path('logout/', views.logout, name='logout'),
]
