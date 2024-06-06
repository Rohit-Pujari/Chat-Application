from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.db import IntegrityError
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            messages.success(request,"You have Succesfuly Logged-In!")
            login(request,user)
            return redirect('chatbox')
        else:
            messages.error(request,"Incorrect Credentials")
            return render(request,"login.html")
    else:
        return render(request,"login.html")



def signUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username Exists')
            return redirect('SignUp')
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email Exists')
            return redirect('SignUp')
        if password1 != password2:
            messages.error('Password must be same')
            return redirect('SignUp')
        if len(password1) < 8:
            messages.error(request,'Password must be 8 Characters')
            return redirect('SignUp')
        user = User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname)
        user.set_password(password1)
        user.save()
        login(request,user)
        return redirect('chatbox')

    return render(request, 'register.html')


def logOut(request):
    logout(request)
    messages.success(request,"You have Logged-out Succesfuly!")
    return render(request,"index.html")

@login_required(login_url='Log-in')
def userprofileEdit(request):
    if request.method == "POST":
        username = request.POST.get('username')
        bio = request.POST.get("bio")
        profile_pic = request.FILES.get("image")
        user = request.user
        try:
            userprofile, created = Profile.objects.get_or_create(user=user)
            userprofile.bio = bio
            if profile_pic:
                userprofile.image = profile_pic
            userprofile.save()
            user.username = username
            user.save()
            return redirect('home')
        except IntegrityError:
            messages.error(request,'Error occured')
            return redirect('home')
    return render(request,'userprofileEdit.html')

@login_required(login_url='Log-in')
def userprofile(request,username):
    user = User.objects.get(username=username)
    context = {
        'userp':user
    }
    return render(request,'userProfile.html',context)