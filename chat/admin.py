from django.contrib import admin
from .models import *

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2')
    search_fields = ('user1', 'user2')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'content', 'timestamp')
    search_fields = ('chat', 'sender', 'content', 'timestamp')