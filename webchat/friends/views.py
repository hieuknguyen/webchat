from django.shortcuts import render
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.
def get_all_friends(request):
    user_id =  int(json.loads(request.COOKIES.get('user')).get('user_id'))
    api_url = "https://quackquack.io.vn/api/friends/get_all_friends.php"
    friends = []
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

@csrf_exempt 
def get_friends(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id', '')
            friend_id = data.get('friend_id', '')
            api_url = "https://quackquack.io.vn/api/friends/get_friends.php"
            try:
                response = requests.post(api_url, data={"user_id": user_id, "friend_id": friend_id})
                if response.status_code == 200:
                    data = response.json()
                    if data.get("isSuccess"):
                        return JsonResponse({
                            'isSuccess': True,
                            'inf': data.get("inf"),
                            'data': data.get("data"),
                        })
                    else:
                        return JsonResponse({
                            'isSuccess': False,
                            'reason': data.get("reason"),
                        })
                else:
                    return JsonResponse({
                        'isSuccess': False,
                        'reason': 'API error',
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
        
@csrf_exempt
def add_friend(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id', '')
            friend_id = data.get('friend_id', '')
            api_url = "https://quackquack.io.vn/api/friends/add_friend.php"
            try:
                response = requests.post(api_url, data={"user_id": user_id, "friend_id": friend_id})
                if response.status_code == 200:
                    data = response.json()
                    if data.get("isSuccess"):
                        return JsonResponse({
                            'isSuccess': True,
                            'message': 'Friend added successfully',
                        })
                    else:
                        return JsonResponse({
                            'isSuccess': False,
                            'reason': data.get("reason") + " " + user_id + " " + friend_id,
                        })
                else:
                    return JsonResponse({
                        'isSuccess': False,
                        'reason': 'API error',
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
    return JsonResponse({
        'isSuccess': False,
        'reason': 'Only POST method is allowed'
    }, status=405)
    
    
    
def get_friends_pending(request):
    user_id =  int(json.loads(request.COOKIES.get('user')).get('user_id'))
    api_url = "https://quackquack.io.vn/api/friends/get_friend_pending.php"
    friends = []
    
    try:
        response = requests.post(api_url, data={"user_id": user_id})
        if response.status_code == 200:
                data = response.json()
                if data.get("isSuccess"):
                    friends = data.get("data")
                    print(friends)
                    return friends
                else:
                    return friends
        else:
            return []
    except requests.exceptions.RequestException as e:
        return []
    
    
@csrf_exempt
def accept_friend(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id', '')
        friend_id = data.get('friend_id', '')
        api_url = "https://quackquack.io.vn/api/friends/accept_friend.php"
        try:
            response = requests.post(api_url, data={"user_id": user_id, "friend_id": friend_id})
            if response.status_code == 200:
                data = response.json()
                if data.get("isSuccess"):
                    return JsonResponse({
                        'isSuccess': True,
                    })
                else:
                    return JsonResponse({
                        'isSuccess': False,
                        'reason': data.get("reason"),
                    })
            else:
                return JsonResponse({
                    'isSuccess': False,
                    'reason': 'API error',
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
    