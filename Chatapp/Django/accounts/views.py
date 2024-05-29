from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import UserForm,UserChangeForm
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
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


def logOut(request):
    logout(request)
    messages.success(request,"You have Logged-out Succesfuly!")
    return render(request,"index.html")