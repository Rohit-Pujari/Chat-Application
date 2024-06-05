from django.urls import path,include
from .views import *
urlpatterns = [
    path('Log-in/',logIn,name='Log-in'),
    path('SignUp/',signUp,name='SignUp'),
    path("SigUp/register/",signUp,name='register'),
    path("Log-in/login/",logIn,name='login'),
    path("logout",logOut,name='logout'),
    path("userprofileEdit/",userprofileEdit,name="userprofileEdit"),
    path('userprofile/<str:username>/',userprofile,name='userprofile')
]

