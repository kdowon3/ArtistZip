# Chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('chatroom/<int:chatroom_id>/', views.chatroom, name='chatroom'),
    path('chatroom/user/<int:user_id>/', views.chatroom_with_user, name='chatroom_with_user'),
]
