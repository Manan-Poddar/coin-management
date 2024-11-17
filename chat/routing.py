from django.urls import path,re_path
from . import consumers

websocket_urlpatterns = [
    # path('ws/wsc/', consumers.MyWebsocketConsumer.as_asgi()),
    path('ws/c-chats/<int:chat_id>/', consumers.ChatConsumer.as_asgi()),
    # re_path(r'ws/c-chats/(?P<room_name>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
]

