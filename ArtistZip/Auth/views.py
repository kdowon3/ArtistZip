from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ArtistSignupForm, GeneralSignupForm
from django.contrib.auth import get_user_model

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        user = authenticate(request, username=user_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': '아이디 또는 비밀번호가 잘못되었습니다.'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def artist_signup(request):
    if request.method == 'POST':
        form = ArtistSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_artist = True
            user.save()
            # 명시적으로 백엔드를 지정하여 로그인
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = ArtistSignupForm()
    return render(request, 'artist_signup_form.html', {'form': form})

def general_signup(request):
    if request.method == 'POST':
        form = GeneralSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # 명시적으로 백엔드를 지정하여 로그인
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = GeneralSignupForm()
    return render(request, 'general_signup_form.html', {'form': form})

def signup(request):
    return render(request, 'login.html')