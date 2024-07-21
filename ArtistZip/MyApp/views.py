# MyApp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artwork
from .forms import ArtworkForm
from Auth.models import CustomUser 
import random
from .models import Portfolio
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactInfoForm
from .models import ContactInfo


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

@login_required
def edit_contact_info(request):
    contact_info, created = ContactInfo.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=contact_info)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Assume you have a profile page
    else:
        form = ContactInfoForm(instance=contact_info)
    
    return render(request, 'edit_contact_info.html', {'form': form})

@csrf_exempt
def portfolio1(request):
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        art_title = request.POST.get('art_title')
        art_description = request.POST.get('art_description')

        portfolio = Portfolio.objects.first()  # assuming there's only one portfolio object
        if not portfolio:
            portfolio = Portfolio()
        portfolio.author_name = author_name
        portfolio.art_title = art_title
        portfolio.art_description = art_description
        portfolio.save()

        return redirect('portfolio1')

    portfolio = Portfolio.objects.first()
    context = {
        'portfolio': portfolio,
    }
    return render(request, 'MyApp/portfolio1.html', context)


def portfolio2(request):
    return render(request, 'MyApp/portfolio2.html')

def portfolio3(request):
    return render(request, 'MyApp/portfolio3.html')

def portfolio4(request):
    return render(request, 'MyApp/portfolio4.html')

def portfolio5(request):
    return render(request, 'MyApp/portfolio5.html')

def portfolio6(request):
    return render(request, 'MyApp/portfolio6.html')

