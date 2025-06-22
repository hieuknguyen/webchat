from django.shortcuts import render
from friends.views import get_friends
import requests
import json
from django.http import JsonResponse
def chat(request):
    friends_list = get_friends(request)
    message = get_message(request,friends_list)
    return render(request, 'index1.html', {'friends': friends_list, "message": message})

def get_message(request, friends_list):
    user_id =  int(json.loads(request.COOKIES.get('user')).get('user_id'))
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
    