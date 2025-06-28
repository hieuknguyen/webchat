from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_form, name='register'),
    path('login/', views.login_form, name='login'),
    path('logout/', views.logout, name='logout'),
    path('seachUsers/', views.seach_users, name='searchUsers'),
    path('profile/', views.profile, name='profile'),
    path('update_avatar/', views.update_avatar, name='update_avatar'),
    path('update_username/', views.update_username, name='update_username'),
    path('check_pass/', views.check_pass, name='check_pass'),
    path('update_pass/', views.update_pass, name='update_pass'),
]
