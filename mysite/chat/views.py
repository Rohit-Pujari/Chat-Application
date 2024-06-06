# chat/views.py
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    chatrooms = request.user.chatrooms.all()
    if chatrooms.exists():
        chatroom = chatrooms.first()
        room_name = chatroom.name
    else:
        chatroom =None
        messages=None
        room_name = None
    context = {
        'rooms':chatrooms,
        'room_name':room_name,
        'chatroom':chatroom,
    }
    return render(request, "chat/chatbox.html",context)

def room(request, room_name):
    chatrooms = request.user.chatrooms.all()
    if chatrooms.exists():
        chatroom = ChatRoom.objects.get(name=room_name)
    else:
        chatroom = None
    context = {
        'rooms':chatrooms,
        'room_name':room_name,
        'chatroom':chatroom
    }
    return render(request, "chat/chatbox.html",context)

@login_required(login_url='Log-in')
def create_group(request):
    if request.method=='POST':
        groupname = request.POST['groupname']
        description = request.POST['description']
        members = request.POST['members']
        member_list = [username.strip() for username in members.split(',')]
        users = []
        for username in member_list:
            try:
                user = User.objects.get(username=username)
                users.append(user.id)
            except User.DoesNOtExist:
                messages.error(f'{user} does not Exist')
                return redirect('chatbox')
        chat_room = ChatRoom.objects.create(name=groupname,is_group=True,description=description)
        chat_room.members.set(users+[request.user.id])
        chat_room.save()
        return redirect('chatroom',chat_room_id=chat_room.name)
    messages.error(request,'Invalid request')
    return redirect('chatbox')

@login_required(login_url='Log-in')
def message_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        message = request.POST['message']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request,f'{user} does not Exist')
            return redirect('chatbox')
        chat_room = ChatRoom.objects.filter(is_group=False, members=user).filter(members=request.user).first()
        if not chat_room:
            chat_room = ChatRoom.objects.create(name=username, is_group=False)
            chat_room.members.set([user, request.user])
            chat_room.save()

        # Create and save the new message
        message_obj = Message.objects.create(sender=request.user, room=chat_room, content=message)
        message_obj.save()

    messages.error(request,'Invalid request')
    return redirect('chatbox')
