# chat/admin.py
from django.contrib import admin
from .models import ChatRoom, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1  # 추가할 빈 메시지 폼의 수
    readonly_fields = ('timestamp',)  # timestamp 필드를 읽기 전용으로 설정

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_participants')
    inlines = [MessageInline]

    def get_participants(self, obj):
        return ", ".join([str(user) for user in obj.participants.all()])
    get_participants.short_description = 'Participants'

class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat_room', 'user', 'content', 'timestamp', 'is_read')
    search_fields = ('user__username', 'content')

admin.site.register(ChatRoom, ChatRoomAdmin)

