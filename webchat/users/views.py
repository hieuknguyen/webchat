from django.shortcuts import render

from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt


def get_home(request):
    return render(request, 'index.html')
def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')
def changepassword(request):
    return render(request,'changepassword.html')

@csrf_exempt
def register_api(request): 
    print("=== ĐÃ VÀO HÀM register_api ===")
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if User.objects.filter(username=username).exists():
                return JsonResponse({"message": "Username đã tồn tại."}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "Email đã được sử dụng."}, status=400)

            User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"message": "Đăng ký thành công."})
        except:
            return JsonResponse({"message": "Lỗi xử lý dữ liệu."}, status=500)

    return JsonResponse({"message": "Chỉ chấp nhận POST."}, status=405)

@csrf_exempt
def login_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            # Tìm user theo email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"message": "Email không tồn tại."}, status=400)

            user_auth = authenticate(username=user.username, password=password)

            if user_auth is not None:
                auth_login(request, user_auth)  # Django login
                return JsonResponse({"message": "Đăng nhập thành công."})
            else:
                return JsonResponse({"message": "Mật khẩu không đúng."}, status=400)

        except Exception as e:
            return JsonResponse({"message": "Lỗi xử lý dữ liệu."}, status=500)

    return JsonResponse({"message": "Chỉ chấp nhận POST."}, status=405)

@csrf_exempt
def change_password_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            newpassword = data.get("newpassword")

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"message": "Email không tồn tại."}, status=400)

            if not user.check_password(password):
                return JsonResponse({"message": "Mật khẩu hiện tại không đúng."}, status=400)

            user.set_password(newpassword)
            user.save()
            return JsonResponse({"message": "Đổi mật khẩu thành công."})

        except Exception as e:
            return JsonResponse({"message": "Lỗi xử lý dữ liệu."}, status=500)

    return JsonResponse({"message": "Chỉ chấp nhận POST."}, status=405)