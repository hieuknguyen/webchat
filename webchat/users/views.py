from django.shortcuts import render

from django.http import JsonResponse
from django.contrib.auth.models import User
import json
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