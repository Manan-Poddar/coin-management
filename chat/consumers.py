from channels.generic.websocket import WebsocketConsumer, AsyncConsumer,AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Websocket Connected ...")
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'
        # Join room group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )
    

    async def receive(self, text_data):
        print("recieve msg from client")
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            user_id = text_data_json['user_id']
            print(text_data, "text data")
            user = await self.get_user(user_id)
            chat = await self.get_chat(self.chat_id)
            print(user, "user",   ">>>>>>", chat, "Chat")
            if chat:
                other_user = chat.user2 if chat.user1 == user else chat.user1
                # Create or retrieve both chat directions
                chat1, chat2 = await self.get_or_create_chats(user, other_user)

                # Save the message to both chats
                message_obj1, message_obj2 = await self.save_message_to_both_chats(chat1, chat2, user, message)
                print("Message Object 1:", message_obj1)
                print("Message Object 2:", message_obj2)

                # Send the message to the WebSocket group
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    {
                        'type': 'chat_message',
                        'message': message_obj1.content,
                        'user': user.first_name,
                        'user_id': user.id,
                        'timestamp': str(message_obj1.timestamp)
                    }
                )
            else:
                print(f"Chat with id {self.chat_id} does not exist.")
        except Exception as e:
            print(f"Error in receive: {e}")

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        user_id = event['user_id']
        timestamp = event['timestamp']
        is_sender = user_id == user_id
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'timestamp': timestamp,
            'is_sender': is_sender
        }))

    @sync_to_async
    def get_user(self, user_id):
        from authentication.models import User
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @sync_to_async
    def get_chat(self, chat_id):
        from .models import Chat
        try:
            chat = Chat.objects.get(id=chat_id)
            print(chat)
            return chat
        except Chat.DoesNotExist:
            return None
    

    @sync_to_async
    def get_or_create_chats(self, user1, user2):
        from .models import Chat

        chat1, created1 = Chat.objects.get_or_create(user1=user1, user2=user2)
        chat2, created2 = Chat.objects.get_or_create(user1=user2, user2=user1)

        return chat1, chat2



    @sync_to_async
    def save_message_to_both_chats(self, chat1, chat2, user, content):
        from .models import Message

        msg1 = Message.objects.create(chat=chat1, sender=user, content=content)
        msg2 = Message.objects.create(chat=chat2, sender=user, content=content)

        return msg1, msg2

    # @sync_to_async
    # def save_message(self, chat, user, content):
    #     from .models import Message
    #     print(chat, "save Messagew ")
    #     msg = Message.objects.create(chat=chat, sender=user, content=content)
    #     msg = Message.objects.create(chat=chat, sender=user, content=content)
    #     return msg

