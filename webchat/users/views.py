from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.test import RequestFactory
from django.http import HttpResponse
import hashlib

import base64
import re
import tempfile
import os
from django.http import JsonResponse
import urllib.parse
from chats.views import chat
def decode_base64_to_temp_file(base64_string: str) -> tempfile._TemporaryFileWrapper | dict:
    if base64_string.startswith("data:image/"):
        match = re.search(r'base64,(.*)', base64_string)
        if match:
            base64_data = match.group(1)
        else:
            print("Lỗi: Chuỗi Base64 không có định dạng Data URL hợp lệ.")
            return {"isSuccess": False, "reason": "Invalid Base64 Data URL format."}
    else:
        base64_data = base64_string

    try:
        decoded_image_data = base64.b64decode(base64_data)
    except base64.binascii.Error as e:
        print(f"Lỗi giải mã Base64: {e}. Chuỗi Base64 có thể không hợp lệ.")
        return {"isSuccess": False, "reason": f"Base64 decoding error: {e}"}
    except Exception as e:
        print(f"Lỗi không xác định khi giải mã Base64: {e}")
        return {"isSuccess": False, "reason": f"Unknown decoding error: {e}"}

    try:
        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        temp_file.write(decoded_image_data)
        temp_file.seek(0)
        print(f"File tạm thời đã tạo và sẵn sàng: {temp_file.name}")
        return temp_file
    except IOError as e:
        print(f"Lỗi khi tạo hoặc ghi file tạm thời: {e}")
        return {"isSuccess": False, "reason": f"Error creating temporary file: {e}"}
    except Exception as e:
        print(f"Lỗi không xác định trong quá trình tạo file tạm thời: {e}")
        return {"isSuccess": False, "reason": f"Unknown error with temporary file: {e}"}


    


@staticmethod
def hash(password: str) -> tuple:
        hash_value = hashlib.sha256(password.encode()).hexdigest()
        return hash_value

def get_home(request):
    user = request.COOKIES.get('user')
    if user:
        try:
            
            return chat(request)
        except json.JSONDecodeError:
            response = redirect('/user/login/')
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
        password = hash(request.POST.get("password"))
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
                        'password': request.POST.get("password")
                    })
                    return login_form(request)
                else:
                    return render(request, 'register.html', {'error': data.get("reason", "Registration failed.")})
            else:
                return render(request, 'register.html', {'error': 'Server error!'})

        except requests.exceptions.RequestException as e:
            return render(request, 'register.html', {'error': 'Unable to connect to registration service.'})

    return render(request, 'register.html', {'user': user if user else None})

@csrf_exempt
def login_form(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = hash(request.POST.get("password"))
        api_url = "https://quackquack.io.vn/api/users/login.php"
        try:
            response = requests.post(api_url, data={"email": email, "password": password})
            
            if response.status_code == 200:
                data = response.json()
                if data.get("isSuccess"):
                    response_redirect = redirect('/chat/')
                
                    user_data_dict = data.get("data") 
                    
                    # Chuyển dictionary thành chuỗi JSON chuẩn (không cần thay thế \054)
                    user_json_string = json.dumps(user_data_dict, separators=(',', ':'))

                    # Mã hóa URL toàn bộ chuỗi JSON
                    encoded_user_cookie = urllib.parse.quote(user_json_string)

                    # Lưu cookie với chuỗi đã mã hóa URL
                    response_redirect.set_cookie('user', encoded_user_cookie)
                    return response_redirect
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
            user_id = json.loads(urllib.parse.unquote(request.COOKIES.get('user'))).get("user_id")
            api_url = "https://quackquack.io.vn/api/friends/seach_users.php"
            try:
                response = requests.post(api_url, data={"username": user_name, "user_id": user_id})
                
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
                            'reason': data.get("reason") + "1",
                        })
                else:
                    return JsonResponse({
                            'isSuccess': False,
                            'reason': "api error" + "2",
                        })
            except requests.exceptions.RequestException as e:
                return JsonResponse({
                            'isSuccess': False,
                            'reason': "api error" + "3",
                        })
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)
            
            
def profile(request):
    return render(request, 'profile.html')


@csrf_exempt
def update_avatar(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        avatar = decode_base64_to_temp_file(data.get('avatar', ''))
        user_id = data.get('user_id', '')
        api_url = "https://quackquack.io.vn/api/users/upload_img.php"
        if isinstance(avatar, dict) and not avatar.get("isSuccess"):
            print("Lỗi khi tạo file tạm thời:", avatar.get("reason"))
        else:
            temp_file_object = avatar
            try:
                files = {
                'image': (
                        os.path.basename(temp_file_object.name),
                        temp_file_object,
                        'image/png'
                )
                }
                data = {'user_id': user_id}

                
                response = requests.post(api_url, data=data, files=files)
                response.raise_for_status()

                api_response = response.json()

                if api_response.get("isSuccess"):
                    return JsonResponse({
                        'isSuccess': True,
                        'imageUrl': api_response.get('imageUrl', ''),
                    })
                    
                else:
                    return JsonResponse({
                        'isSuccess': False,
                        'reason': api_response.get('reason', 'Failed to upload image'),
                    })

            except requests.exceptions.RequestException as e:
                return JsonResponse({
                    'isSuccess': False,
                    'reason': f"API error: {e}",
                })
            except json.JSONDecodeError:
                return JsonResponse({
                    'isSuccess': False,
                    'reason': 'Error decoding JSON response from API',
                })
            finally:
                temp_file_object.close()
                os.remove(temp_file_object.name)
                print(f"File tạm thời '{temp_file_object.name}' đã được đóng và xóa.")

@csrf_exempt
def update_username(request):
    if request.method == 'POST':
        try:
            # Đọc JSON từ request body
            data = json.loads(request.body)
            user_name = data.get('username', '')
            user_id = data.get('user_id', '')
            api_url = "https://quackquack.io.vn/api/users/update_name.php"
            try:
                response = requests.post(api_url, data={"username": user_name, "user_id": user_id})
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("isSuccess"):
                        return JsonResponse({
                            'isSuccess': True,
                        })
                    else:
                        return JsonResponse({
                            'isSuccess': False,
                            'reason': data.get("reason") + "1",
                        })
                else:
                    return JsonResponse({
                            'isSuccess': False,
                            'reason': "api error" + "2",
                        })
            except requests.exceptions.RequestException as e:
                return JsonResponse({
                            'isSuccess': False,
                            'reason': "api error" + "3",
                        })
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)
    

@csrf_exempt
def check_pass (request):
    if request.method == 'POST':
        try:
            # Đọc JSON từ request body
            data = json.loads(request.body)
            password = hash(data.get("password"))
            email = data.get('email', '')
            print(password+email)

            api_url = "https://quackquack.io.vn/api/users/check_password.php"
            try:
                response = requests.post(api_url, data={"password": password, "email": email})
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("isSuccess"):
                        return JsonResponse({
                            'isSuccess': True,
                        })
                    else:
                        return JsonResponse({
                            'isSuccess': False,
                            'reason': data.get("reason") + "1",
                        })
                else:
                    return JsonResponse({
                            'isSuccess': False,
                            'reason': "api error" + "2",
                        })
            except requests.exceptions.RequestException as e:
                print(e)
                return JsonResponse({
                            'isSuccess': False,
                            'reason': "api error" + "3",
                        })
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)

    
@csrf_exempt    
def update_pass(request):
    if request.method == 'POST':
        try:
            # Đọc JSON từ request body
            data = json.loads(request.body)
            password = hash(data.get("password"))
            email = data.get('email', '')
            print(password+email)

            api_url = "https://quackquack.io.vn/api/users/update_password.php"
            try:
                response = requests.post(api_url, data={"password": password, "email": email})
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("isSuccess"):
                        return JsonResponse({
                            'isSuccess': True,
                        })
                    else:
                        return JsonResponse({
                            'isSuccess': False,
                            'reason': data.get("reason") + "1",
                        })
                else:
                    return JsonResponse({
                            'isSuccess': False,
                            'reason': "api error" + "2",
                        })
            except requests.exceptions.RequestException as e:
                print(e)
                return JsonResponse({
                            'isSuccess': False,
                            'reason': "api error" + "3",
                        })
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)
    
    