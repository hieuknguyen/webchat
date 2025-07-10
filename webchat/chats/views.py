from django.shortcuts import render
from friends.views import get_all_friends, get_friends_pending
import requests
import json
from django.http import JsonResponse
from django.http import HttpResponse
import urllib.parse
from django.views.decorators.csrf import csrf_exempt

def chat(request):
  
   
    friends_list = get_all_friends(request)
    friends_list_pending = get_friends_pending(request)
    message = get_message(request,friends_list)
    
    return render(request, 'chat.html', {'friends': friends_list,'friends_list_pending':friends_list_pending, "message": message})

def get_message(request, friends_list):
    user_id = json.loads(urllib.parse.unquote(request.COOKIES.get('user'))).get("user_id")
    print("="*100)
    data1 = []
    for i in friends_list:
        api_url = "https://quackquack.io.vn/api/chats/get_message.php"
        try:
            response = requests.post(api_url, data={"user_id": user_id, "friend_id": i.get("user_id")})
            
            if response.status_code == 200:
                    data = response.json()
                    if data.get("isSuccess"):
                        data1.append({"friend_id": i.get("user_id"), "chat_list": data.get("data")})
                    else:
                        pass
            else:
                pass
        except requests.exceptions.RequestException as e:
            pass 
    return data1



@csrf_exempt
def send_audio(request):
    if request.method == 'POST':
        audio = request.FILES.get('audio')
        if audio:
            api_url = "https://quackquack.io.vn/api/chats/send_audio.php"
            try:
                # Đúng cú pháp gửi file với multipart/form-data
                files = {'audio': (audio.name, audio.file, audio.content_type)}
                response = requests.post(api_url, files=files)

                if response.status_code == 200:
                    data = response.json()
                    if data.get("isSuccess"):
                        return JsonResponse({"isSuccess": True, "data": data.get("file")})
                    else:
                        return JsonResponse({"isSuccess": False, "reason": data.get("reason")})
                else:
                    return JsonResponse({"isSuccess": False, "reason": "API upload failed"})
            except requests.exceptions.RequestException as e:
                return JsonResponse({"isSuccess": False, "reason": "Connection error"})

        return JsonResponse({"isSuccess": False, "reason": "No audio file found"})
    
    return JsonResponse({"isSuccess": False, "reason": "Invalid method"})

@csrf_exempt
def uploads_img(request):
    if request.method == 'POST':
      
        image = request.FILES.get('img')
        if image:
            api_url = "https://quackquack.io.vn/api/chats/upload_img.php"
            
            try:
              
                image.seek(0)
                
             
                files = {'photo': (image.name, image.file, image.content_type)}
                
                
                
                response = requests.post(api_url, files=files)

              
                if response.status_code == 200:
                    api_response_data = response.json()
                    
                    
                    if api_response_data.get("status") == "success":
                      
                        return JsonResponse({"isSuccess": True, "data": api_response_data.get("data").get("file_url")})
                    else:
                        
                        return JsonResponse({"isSuccess": False, "reason": api_response_data.get("message")})
                else:
                    print(f"Lỗi từ PHP - Status Code: {response.status_code}")
                    print(f"Lỗi từ PHP - Nội dung: {response.text}")
                    return JsonResponse({"isSuccess": False, "reason": "API analyze failed"})
            
            except requests.exceptions.RequestException as e:
                
                return JsonResponse({"isSuccess": False, "reason": "Connection error"})

       
        return JsonResponse({"isSuccess": False, "reason": "No image file found"})
    
    
    return JsonResponse({"isSuccess": False, "reason": "Invalid method"})