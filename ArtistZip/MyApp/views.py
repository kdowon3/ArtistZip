from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artwork, Portfolio, ContactInfo
from .forms import ArtworkForm, PortfolioForm, ContactInfoForm
from Auth.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
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

@login_required
def edit_contact_info(request):
    contact_info, created = ContactInfo.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=contact_info)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=request.user.id)  # Redirect to profile page
    else:
        form = ContactInfoForm(instance=contact_info)
    
    return render(request, 'edit_contact_info.html', {'form': form})

@login_required
@csrf_exempt
def handle_portfolio(request, user_id=None, id=None, template_name='MyApp/portfolio1.html'):
    if id:
        portfolio = get_object_or_404(Portfolio, id=id)
    else:
        portfolio = Portfolio()

    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()

            # Handle ContactInfo
            contact_info, created = ContactInfo.objects.get_or_create(user=request.user)
            contact_form = ContactInfoForm(request.POST, instance=contact_info)
            if contact_form.is_valid():
                contact_form.save()

            # Handle Artwork uploads
            for i in range(1, 7):
                image_file = request.FILES.get(f'image{i}')
                if image_file:
                    artwork = Artwork(
                        user=request.user,
                        artwork_image=image_file,
                        artwork_title=f'Artwork {i}',  # Placeholder title
                        artwork_description=f'Description for artwork {i}'  # Placeholder description
                    )
                    artwork.save()

            return redirect('myprofile', user_id=user_id)
    else:
        form = PortfolioForm(instance=portfolio)

    contact_info = ContactInfo.objects.filter(user=request.user).first()
    artworks = Artwork.objects.filter(user=request.user)

    context = {
        'form': form,
        'contact_info': contact_info,
        'artworks': artworks,
    }
    return render(request, template_name, context)

# Define the portfolio views to use the `handle_portfolio` function
@login_required
def portfolio1(request, user_id=None, id=None):
    return handle_portfolio(request, user_id, id, 'MyApp/portfolio1.html')

@login_required
def portfolio2(request, user_id=None, id=None):
    return handle_portfolio(request, user_id, id, 'MyApp/portfolio2.html')

@login_required
def portfolio3(request, user_id=None, id=None):
    return handle_portfolio(request, user_id, id, 'MyApp/portfolio3.html')

@login_required
def portfolio4(request, user_id=None, id=None):
    return handle_portfolio(request, user_id, id, 'MyApp/portfolio4.html')

@login_required
def portfolio5(request, user_id=None, id=None):
    return handle_portfolio(request, user_id, id, 'MyApp/portfolio5.html')

@login_required
def portfolio6(request, user_id=None, id=None):
    return handle_portfolio(request, user_id, id, 'MyApp/portfolio6.html')

