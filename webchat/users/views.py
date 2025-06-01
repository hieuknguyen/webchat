from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from .logger import logger

def get_home(request):
    return render(request, 'index.html')



@csrf_exempt
def register_form(request):
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

            logger.info(f"Register request: {response.request.body}")

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Register response: {data}")
                if data.get("isSuccess"):
                    return render(request, 'register.html', {'message': 'User registered successfully!'})
                else:
                    return render(request, 'register.html', {'error': data.get("reason", "Registration failed.")})
            else:
                return render(request, 'register.html', {'error': 'Server error!'})

        except requests.exceptions.RequestException as e:
            logger.error("Register API error: %s", str(e))
            return render(request, 'register.html', {'error': 'Unable to connect to registration service.'})

    return render(request, 'register.html')


def login_form(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        api_url = "https://quackquack.io.vn/api/users/login.php"
        try:
            response = requests.post(api_url, data={
                "email": email,
                "password": password
            })

            logger.info(f"Login request: {response.request.body}")


            if response.status_code == 200:
                data = response.json()
                logger.info(f"Login response: {data}")
                if data.get("isSuccess"):
                    return render(request, 'login.html', {'message': 'Login successful'})
                else:
                    return render(request, 'login.html', {'error': data.get("reason", "Login failed")})
            else:
                return render(request, 'login.html', {'error': 'API login failed'})

        except requests.exceptions.RequestException as e:
            logger.error("Login API error: %s", str(e)) 
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

