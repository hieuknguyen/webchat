from django.urls import path
from . import views

urlpatterns = [
    path('send_audio/', views.send_audio, name='send_audio'),
    path('uploads_img/', views.uploads_img, name='uploads_img'),
]
