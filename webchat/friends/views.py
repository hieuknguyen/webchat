from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
# Create your views here.
def get_friends(request):
    user_id =  int(json.loads(request.COOKIES.get('user')).get('user_id'))
    api_url = "https://quackquack.io.vn/api/friends/get_friends.php"
    try:
        response = requests.post(api_url, data={"user_id": user_id})
        if response.status_code == 200:
                data = response.json()
                if data.get("isSuccess"):
                    friends = data.get("data")
                    return friends
                else:
                    return friends
        else:
            return []
    except requests.exceptions.RequestException as e:
        return []   
        
