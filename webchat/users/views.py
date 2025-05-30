from django.shortcuts import render
def get_home(request):
    return render(request, 'index.html')
# Create your views here.