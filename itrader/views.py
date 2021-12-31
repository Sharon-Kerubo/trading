from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return render(request, "itrader/index.html")

def login(request):
    return render(request,  "itrader/login.html")

def register(request):
    # form = UserCreationForm()
    # context = {'form': form}
    return render(request,  "itrader/login.html") 
    # context)
