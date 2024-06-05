# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="chatbox"),
    path('chatroom/<str:room_name>/',views.room,name="chatroom"),
    path('messageUser/', views.message_user, name='messageUser'),
    path('createGroup/', views.create_group, name='createGroup'),
]