from django.shortcuts import render
def get_home(request):
    return render(request, 'index.html')
def login(request):
    return render(request,'login.html')
def register(request):
    return render(request,'register.html')
def changepassword(request):
    return render(request,'changepassword.html')
# Create your views here.
