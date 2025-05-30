from django.contrib import admin
from django.urls import path, include
from users import views as user
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user.get_home, name='user'),
    path('login/',user.login),
    path('api/login/', user.login_api),  
    path('register/',user.register),
    path('api/register/', user.register_api),
    path('changepassword/',user.changepassword),
    path('api/changepassword/', user.change_password_api),

]
