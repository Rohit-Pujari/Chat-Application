from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')

def about(request):
    return render(request,'aboutUs.html')

def contact(request):
    return render(request,'contact.html')