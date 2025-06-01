from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
def get_home(request):
    user = request.COOKIES.get('user')
    if user:
        try:
            user_data = json.loads(user)
            return render(request, 'index.html', {'user': user_data})
        except json.JSONDecodeError:
            return render(request, 'index.html', {'error': 'Invalid user data in cookie.'})
    return render(request, 'index.html')



@csrf_exempt
def register_form(request):
    user = request.COOKIES.get('user')
    
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        api_url = "https://quackquack.io.vn/api/users/register.php"

        try:
            response = requests.post(api_url, data={
                "username": username,
                "email": email,
                "password": password
            })


            if response.status_code == 200:
                data = response.json()
                if data.get("isSuccess"):
                    return render(request, 'register.html', {'message': 'User registered successfully!'})
                else:
                    return render(request, 'register.html', {'error': data.get("reason", "Registration failed.")})
            else:
                return render(request, 'register.html', {'error': 'Server error!'})

        except requests.exceptions.RequestException as e:
            return render(request, 'register.html', {'error': 'Unable to connect to registration service.'})

    return render(request, 'register.html', {'user': json.loads(user) if user else None})


def login_form(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        api_url = "https://quackquack.io.vn/api/users/login.php"
        try:
            response = requests.post(api_url, data={"email": email, "password": password})
            
            if response.status_code == 200:
                data = response.json()
                if data.get("isSuccess"):
                    response = render(request, 'index.html', {'message': 'Login successful', 'user': data.get("data")})
                    response.set_cookie('user', data.get("data"))
                    return response
                else:
                    return render(request, 'login.html', {'error': data.get("reason", "Login failed")})
            else:
                return render(request, 'login.html', {'error': 'API login failed'})

        except requests.exceptions.RequestException as e:
            return render(request, 'login.html', {'error': 'Unable to connect to login service.'})
    return render(request, 'login.html')


# test
# url = "https://quackquack.io.vn/api/users/login.php"
# response = requests.post(url, json={
#                 "email": nguyentrunghieu4390@gmail.com,
#                 "password": hieuknguyen12
#             })
# if response.status_code == 200:
#     data = response.json()
#     if data.get("isSuccess"):
#         print("Login successful")
#     else:
#         print("Login failed:", data.get("reason", "Unknown error"))

