# MyApp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artwork
from .forms import ArtworkForm
from Auth.models import CustomUser
from Chat.models import ChatRoom, Message
from django.contrib.auth import get_user_model
import random
from django.db.models import Q

User = get_user_model()

def index(request):
    return render(request, 'MyApp/index.html')

def az(request):
    return render(request, 'MyApp/az.html')

def artists(request):
    return render(request, 'MyApp/artists.html')

def gallery(request):
    artworks = list(Artwork.objects.all())
    random.shuffle(artworks)
    return render(request, 'MyApp/gallery.html', {'artworks': artworks})

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
    context = {
        'user': user,
        'artworks': artworks,
    }
    return render(request, 'MyApp/myprofile.html', context)

@login_required
def template(request, user_id):
    user = get_object_or_404(User, id=user_id)
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

@login_required
def delete_artwork(request):
    if request.method == 'GET' and 'id' in request.GET:
        artwork_id = request.GET['id']
        artwork = get_object_or_404(Artwork, id=artwork_id)
        user_id = artwork.user.id
        artwork.delete()
        return redirect('myprofile', user_id=user_id)
    return redirect('myprofile')
