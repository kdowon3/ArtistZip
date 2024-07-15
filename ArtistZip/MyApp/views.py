# MyApp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artwork
from .forms import ArtworkForm
from Auth.models import CustomUser 


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

@login_required
def myprofile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    artworks = Artwork.objects.filter(user=user)
    context = {
        'user': user,
        'artworks': artworks,
    }
    return render(request, 'MyApp/myprofile.html', context)

@login_required
def template(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.user = user
            artwork.save()
            messages.success(request, '작품이 성공적으로 저장되었습니다.')
            return redirect('myprofile', user_id=user.id)
        else:
            messages.error(request, '저장 중 오류가 발생했습니다.')
    else:
        form = ArtworkForm()
    context = {
        'form': form,
    }
    return render(request, 'MyApp/template.html', context)