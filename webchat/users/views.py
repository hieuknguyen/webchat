from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import requests
def get_home(request):
    user = request.COOKIES.get('user')
    if user:
        try:
            response = render(request, 'index.html', {'user': user})
            return response
        except json.JSONDecodeError:
            response = redirect('/user/')
            return response
    else:
        response = redirect('/user/login/')
        return response



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

    return render(request, 'register.html', {'user': user if user else None})


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
                    response = redirect('/chat/')
                    response.set_cookie('user', json.dumps(data.get("data")))
                    return response
                else:
                    return render(request, 'login.html', {'error': data.get("reason", "Login failed")})
            else:
                return render(request, 'login.html', {'error': 'API login failed'})
        except requests.exceptions.RequestException as e:
            return render(request, 'login.html', {'error': 'Unable to connect to login service.'})
    if request.COOKIES.get('user'):
        return redirect('/chat/')
    return render(request, 'login.html')
def logout(request):
    response = redirect('/user/')
    response.delete_cookie('user')
    return response



