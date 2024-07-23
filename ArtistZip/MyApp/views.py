# MyApp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artwork, Portfolio, ContactInfo
from .forms import ArtworkForm, PortfolioForm, ContactInfoForm
from Auth.models import CustomUser
from Chat.models import ChatRoom, Message
from django.contrib.auth import get_user_model
import random
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()

def index(request):
    return render(request, 'MyApp/index.html')

def az(request):
    return render(request, 'MyApp/az.html')
@login_required
def artists(request):
    search_query = request.GET.get('search', '')
    if search_query:
        artists_queryset = CustomUser.objects.filter(
            Q(username__icontains=search_query) & Q(is_artist=True)
        )
    else:
        artists_queryset = CustomUser.objects.filter(is_artist=True)
    
    artists = list(artists_queryset)  # QuerySet을 리스트로 변환
    random.shuffle(artists)
    
    context = {
        'artists': artists,
        'search_query': search_query,
    }
    return render(request, 'MyApp/artists.html', context)
@login_required
def gallery(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        artworks = list(Artwork.objects.filter(
            Q(user__username__icontains=search_query) |
            Q(artwork_title__icontains=search_query)
        ))
    else:
        artworks = list(Artwork.objects.all())
    
    random.shuffle(artworks)
    
    context = {
        'artworks': artworks,
        'search_query': search_query,
    }
    return render(request, 'MyApp/gallery.html', context)

@login_required
def contact(request):
    chatrooms = ChatRoom.objects.filter(participants=request.user)
    for chatroom in chatrooms:
        chatroom.last_message = chatroom.messages.last()
        chatroom.last_message_time = chatroom.last_message.timestamp if chatroom.last_message else None
        chatroom.unread = chatroom.messages.filter(is_read=False).exclude(user=request.user).exists()

    active_chatroom = None
    messages = None
    other_user = None
    chatroom_id = request.GET.get('chatroom_id')
    if chatroom_id:
        active_chatroom = get_object_or_404(ChatRoom, id=chatroom_id, participants=request.user)
        messages = Message.objects.filter(chat_room=active_chatroom).order_by('timestamp')
        # Update the 'is_read' field for messages not sent by the current user
        Message.objects.filter(chat_room=active_chatroom).filter(~Q(user=request.user)).update(is_read=True)
        other_user = active_chatroom.get_other_user(request.user)

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat_room=active_chatroom, user=request.user, content=content)
            return redirect(f'/contact/?chatroom_id={chatroom_id}')

    return render(request, 'MyApp/contact.html', {
        'chatrooms': chatrooms,
        'active_chatroom': active_chatroom,
        'messages': messages,
        'other_user': other_user
    })


    
def signup(request):
    return render(request, 'MyApp/signup.html')

def login(request):
    return render(request, 'MyApp/login.html')
@login_required
def profile(request, user_id):
    profile_user = get_object_or_404(CustomUser, id=user_id)
    artworks = Artwork.objects.filter(user=profile_user)
    # 기존에 이 두 사용자 간의 채팅방이 있는지 확인
    chatroom = ChatRoom.objects.filter(participants__id=profile_user.id).filter(participants__id=request.user.id).first()
    if not chatroom:
        chatroom = ChatRoom.objects.create()
        chatroom.participants.add(request.user, profile_user)
    return render(request, 'MyApp/profile.html', {
        'profile_user': profile_user,
        'artworks': artworks,
        'chatroom_id': chatroom.id
    })

@login_required
def myprofile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    artworks = Artwork.objects.filter(user=user)
    followed_artists = user.following.all()
    context = {
        'user': user,
        'artworks': artworks,
        'followed_artists': followed_artists,
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
@login_required
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
        portfolio = Portfolio(user=request.user) 

    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user  # Ensure the user is set
            portfolio.save()

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

