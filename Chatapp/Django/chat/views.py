from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
# Create your views here.
@login_required
def chatlist(request):
    chatrooms = request.user.chatrooms.all()
    if chatrooms.exists(): 
        chatroom = chatrooms.first()
        messages = chatroom.messages.all() 
    else:
        chatroom = None
        messages = None
    
    context = {
        'rooms': chatrooms,
        'chatroom': chatroom,
        'messages': messages
    }
    return render(request, 'chatbox.html', context)
@login_required
def chatroom(request,chat_room_id):
    room = ChatRoom.objects.get(id=chat_room_id)
    chatrooms = request.user.chatrooms.all()
    messages = Message.objects.filter(room=chat_room_id)
    context = {
        'rooms':chatrooms,
        'chatroom':room,
        'messages':messages
    }
    return render(request,'chatbox.html',context)

@login_required
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
                message.error(f'{user} does not Exist')
                return redirect('chatbox')
        chat_room = ChatRoom.objects.create(name=groupname,is_group=True)
        chat_room.members.set(users+[request.user.id])
        chat_room.save()
        return redirect('chatroom',chat_room_id=chat_room.id)
    message.error('Invalid request')
    return redirect('chatbox')

@login_required
def message_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        message = request.POST['message']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            message.error(f'{user} does not Exist')
            return redirect('chatbox')
        chat_room = ChatRoom.objects.create(name=username,is_group=False)
        chat_room.members.set([user.id,request.user.id])
        chat_room.save()
        Message.objects.create(sender=request.user,room=chat_room,content=message)
        Message.save()
        return redirect('chatroom',room_id=chat_room.id)
    message.error('Invalid request')
    return redirect('chatbox')

@login_required
def sendmessage(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
    if request.method == 'POST':
        message_content = request.POST['message']
        if len(message_content.strip()) == 0:
            messages.error(request, 'Cannot send empty message.')
            return redirect('chatroom',room_id=chat_room_id)
        Message.objects.create(sender=request.user, room=chat_room, content=message_content)
        return redirect('chatroom', chat_room_id=chat_room_id)
    
    return redirect('chatroom', chat_room_id=chat_room_id)