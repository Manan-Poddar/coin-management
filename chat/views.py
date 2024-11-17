from django.shortcuts import render, get_object_or_404, redirect
from authentication.models import User
from .models import Chat, Message
from django.http import JsonResponse

def get_or_create_chat(user1, user2):
    print(user1, user2)
    chat, created = Chat.objects.get_or_create(user1=user1, user2=user2)
    if not created:
        chat, created = Chat.objects.get_or_create(user1=user2, user2=user1)
    return chat

def chat_view(request, request_user_id):
    request_user = get_object_or_404(User, id=request_user_id)

    logged_user_id = request.session.get('user_id', None)
    logged_user = get_object_or_404(User, id=logged_user_id)
    chat = get_or_create_chat(logged_user, request_user)
    messages = chat.messages.order_by('-timestamp')[:50]  # Load last 50 messages
    context = {
        'request_user': request_user,
        'current_user': logged_user,
        'messages': messages,
        'chat_id': chat.id,
    }
    return render(request, 'chat_room.html', context)


def load_more_messages(request):
    chat_id = request.GET.get('chat_id')
    last_message_id = request.GET.get('last_message_id')
    print(last_message_id, "Last Message Id")
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.filter(id__lt=last_message_id).order_by('-timestamp')[:20]

    message_list = [
        {
            'id': message.id,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'sender': message.sender.first_name,
        }
        for message in messages
    ]
    return JsonResponse({'messages': message_list})
