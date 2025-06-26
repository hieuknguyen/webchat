from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.test import RequestFactory
from django.http import HttpResponse
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
                    factory = RequestFactory()
                    request = factory.post('/login/', data={
                        'email': email,
                        'password': password
                    })
                    return login_form(request)
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



@csrf_exempt  
def seach_users(request):
    import json
    from django.http import JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    if request.method == 'POST':
        try:
            # Đọc JSON từ request body
            data = json.loads(request.body)
            user_name = data.get('username', '')
            api_url = "https://quackquack.io.vn/api/friends/seach_users.php"
            try:
                response = requests.post(api_url, data={"username": user_name})
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("isSuccess"):
                        return JsonResponse({
                            'isSuccess': True,
                            'data': response.json().get("data", []),
                        })
                    else:
                        return JsonResponse({
                            'isSuccess': False,
                            'reason': "api error",
                        })
                else:
                    return JsonResponse({
                            'isSuccess': False,
                            'reason': "api error",
                        })
            except requests.exceptions.RequestException as e:
                return JsonResponse({
                            'isSuccess': False,
                            'reason': "api error",
                        })
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)