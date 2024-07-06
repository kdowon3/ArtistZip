# MyApp/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'MyApp/index.html')

def az(request):
    return render(request, 'MyApp/az.html')

def artists(request):
    return render(request, 'MyApp/artists.html')

def gallery(request):
    return render(request, 'MyApp/gallery.html')

def contact(request):
    return render(request, 'MyApp/contact.html')

def signup(request):
    return render(request, 'MyApp/signup.html')

def login(request):
    return render(request, 'MyApp/login.html')

def profile(request):  # profile 뷰 함수 추가
    return render(request, 'MyApp/profile.html')

def myprofile(request):  # profile 뷰 함수 추가
    return render(request, 'MyApp/myprofile.html')

def template(request):  # profile 뷰 함수 추가
    return render(request, 'MyApp/template.html')