# Chat/utils.py

from .models import ChatRoom

def create_or_get_chatroom(user1, user2):
    chat_room = ChatRoom.objects.filter(participants=user1).filter(participants=user2).first()
    if not chat_room:
        chat_room = ChatRoom.objects.create()
        chat_room.participants.add(user1, user2)
    return chat_room
