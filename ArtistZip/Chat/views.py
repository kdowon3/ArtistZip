# Chat/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from .utils import create_or_get_chatroom
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chatroom(request, chatroom_id):
    chat_room = get_object_or_404(ChatRoom, id=chatroom_id, participants=request.user)
    other_user = chat_room.participants.exclude(id=request.user.id).first()
    
    messages = Message.objects.filter(chat_room=chat_room).order_by('timestamp')
    
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat_room=chat_room, user=request.user, content=content)
            return redirect('chatroom', chatroom_id=chatroom_id)

    return render(request, 'chatroom.html', {
        'chat_room': chat_room,
        'other_user': other_user,
        'messages': messages,
    })

@login_required
def chatroom_with_user(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    chat_room = create_or_get_chatroom(request.user, other_user)
    return redirect('chatroom', chatroom_id=chat_room.id)
