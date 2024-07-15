# MyApp/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'MyApp/index.html')


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

def profile(request):
    return render(request, 'MyApp/profile.html')

def myprofile(request):
    return render(request, 'MyApp/myprofile.html')
