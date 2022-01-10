from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required
from trading import settings
from django.core.mail import send_mail

def home(request):
    return render(request, "itrader/home.html")

def itrader(request):
    return render(request, "itrader/itrader.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return render(request, "itrader/itrader.html", {'username':username}) 
        else: 
            messages.error(request, "Bad Credentials")
            return render(request,  "itrader/home.html")
    return render(request,  "itrader/auth.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2= request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try another username")
            return redirect('/')
        if User.objects.filter(username=username):
            messages.error(request, "Email already registered")
            return redirect('/')
        if len(username)>10:
            messages.error(request, "Username must be less that 10 characters")
        if password1 != password2:
            messages.error(request, "Passwwords didn't match")
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-numeric")
            return redirect('/')

        user = User.objects.create_user(username, email, password1)
        user.email = email
        user.save()

        messages.success(request, "Your Account has been successfully created")

        #Welcome Email
        subject = "Welcome to iTrader"
        message = "Hello " + user.username + "! \n" + "Welcome to iTrader! \n We have sent you a confirmation email, please confirm your emaul address in order to activate your account. \n \n Thank you \n iTrader"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect("/signin")
    return render(request,  "itrader/auth.html") 

@login_required
def logout(request):
    django_logout(request)
    return redirect('/')
      


    
