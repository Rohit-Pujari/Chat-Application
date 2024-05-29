from django.urls import path
from .views import *
from .models import *

urlpatterns = [
    path("",chatlist,name='chatbox'),
    path('chatroom<int:chat_room_id>',chatroom,name="chatroom"),
    path('messageUser',message_user,name="messageUser"),
    path('createGroup',create_group,name='createGroup'),
    path('sendmessage<int:chat_room_id>',sendmessage,name='sendmessage'),
]
