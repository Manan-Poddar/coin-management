from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('chats/<int:request_user_id>/', views.chat_view, name='chat-view'),
    path('load_more_messages/', views.load_more_messages, name='load-more-messages'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
