# MyApp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artwork
from .forms import ArtworkForm
from Auth.models import CustomUser 
import random


def index(request):
    return render(request, 'MyApp/index.html')

def az(request):
    return render(request, 'MyApp/az.html')

def artists(request):
    return render(request, 'MyApp/artists.html')

def gallery(request):
    artworks = list(Artwork.objects.all())  # QuerySet을 리스트로 변환
    random.shuffle(artworks)  # 리스트를 섞음
    return render(request, 'MyApp/gallery.html', {'artworks': artworks})

def contact(request):
    return render(request, 'MyApp/contact.html')

def signup(request):
    return render(request, 'MyApp/signup.html')

def login(request):
    return render(request, 'MyApp/login.html')

def profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    artworks = Artwork.objects.filter(user=user)
    return render(request, 'MyApp/profile.html', {'user': user, 'artworks': artworks})

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

def edit_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            form.save()
            return redirect('myprofile', user_id=artwork.user.id)
    else:
        form = ArtworkForm(instance=artwork)
    
    context = {
        'form': form
    }
    return render(request, 'MyApp/template.html', context)

def delete_artwork(request):
    if request.method == 'GET' and 'id' in request.GET:
        artwork_id = request.GET['id']
        artwork = get_object_or_404(Artwork, id=artwork_id)
        user_id = artwork.user.id
        artwork.delete()
        return redirect('myprofile', user_id=user_id)
    return redirect('myprofile')

def simple_template1(request):
    return render(request, 'MyApp/simple_template1.html')