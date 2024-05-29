from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password1','password2')

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')