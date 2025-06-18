from django.shortcuts import render
from friends.views import get_friends
def chat(request):
    get_friends_list = get_friends(request)
    return render(request, 'index1.html', {'friends': get_friends_list})

