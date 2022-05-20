from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required
from urllib3 import HTTPResponse
from trading import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
import json, psycopg2
from .models import Message, Room, StockData, Trade, News, CompanyProfile
from django.contrib.auth.models import User


def home(request):
    return render(request, "itrader/home.html")

def contactus(request):
    return render(request, "itrader/contactus.html")

def aboutus(request):
    return render(request, "itrader/aboutus.html")

def news(request):
    
    news_articles = News.objects.order_by('-date')
    topics = StockData.objects.all()
    return render(request, 'itrader/news.html', {'news_articles': news_articles, 'topics':topics})

def dashboard(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    activetrades = Trade.objects.all()
    return render(request, "itrader/dashboard.html", {'username':username, 'activetrades':activetrades})

def room(request, roomname):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    rooms = StockData.objects.all()
    messages = Message.objects.order_by('room')
    return render(request, 'itrader/room.html', {'roomname': roomname, 'username':username, 'messages': messages, 'rooms':rooms})

def chat(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    rooms = StockData.objects.all()
    messages = Message.objects.all()
    return render(request, "itrader/chat.html", {'username':username, 'rooms':rooms, 'messages': messages})

def buysell(request):
    if request.method == "POST":
        username = request.POST['clientcode']
        buysell = request.POST['buysell']
        security = request.POST['security']
        market = request.POST['market']
        quantity = request.POST['quantity']
        price = request.POST['price']
        validupto = request.POST['validupto']
        delivery = request.POST['delivery']

        trade = Trade.objects.create(clientcode=User.objects.get(username= username), buysell=buysell, security=StockData.objects.get(security=security), market=market, quantity=quantity,price=price,validupto=validupto,delivery=delivery)
        trade.save()
        return render(request, "itrader/itrader.html")


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/itrader') 
        else: 
            messages.error(request, "Invalid Login")
    return render(request,  "itrader/auth.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2= request.POST['password2']

        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try another username")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        elif len(username)>20:
            messages.error(request, "Username must be less that 20 characters")
        elif password1 != password2:
            messages.error(request, "Passwwords didn't match")
        elif not username.isalnum():
            messages.error(request, "Username must be Alpha-numeric")
        else:
            user = User.objects.create_user(username, email, password1)
            user.is_active = False
            user.save()

            messages.success(request, "Your Account has been successfully created. We have sent you a confirmation email, please confirm your email address in order to activate your account.")

            #Welcome Email
            subject = "Welcome to iTrader"
            message = "Hello " + user.username + "! \n" + "Welcome to iTrader! \nWe have sent you a confirmation email, please confirm your email address in order to activate your account. \n \nThank you \niTrader"
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            #Email Address confirmation
            current_site = get_current_site(request)
            email_subject = "Confirm your email!!"
            message2 = render_to_string("itrader/email_confirmation.html",{
                'name': user.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True
            email.send()

            return redirect("/signin")
    return render(request,  "itrader/auth.html") 

@login_required
def logout(request):
    django_logout(request)
    return redirect('/home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotEXist):
        user = None
    
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, "itrader/itrader.html") 
    else:
        return render(request, 'itrader/activation_failed.html')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    current_site = get_current_site(request)
                    email_subject = "Password Reset Requested"
                    reset_message = render_to_string("itrader/password/password_reset_email.txt",{
                        'name': user.username,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    })
                    email = EmailMessage(
                        email_subject,
                        reset_message,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                    )
                    email.fail_silently = True
                    email.send()
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="itrader/password/password_reset.html", context={"password_reset_form":password_reset_form})

def itrader(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    try:
        #connect to the db
        con = psycopg2.connect(
            host = 'localhost',
            database = 'trading',
            user = 'postgres',
            password = 'postgres',
            port = 5432
        )

        #cursor
        cur = con.cursor()
        #execute querys
        cur .execute("select array_to_json(array_agg(row_to_json(stockdata))) from(select security,lastprice,demandqty,demandprice, supplyprice,supplyqty,lastqty,high,low from itrader_stockdata) stockdata")
        data = cur.fetchone()
        data = json.dumps(data[0])
        cur.execute("select array_to_json(array_agg(row_to_json(companyprofile))) from(select security,profile from itrader_companyprofile) companyprofile")
        profile = cur.fetchone()
        profile = json.dumps(profile[0])
        cur.execute("select array_to_json(array_agg(row_to_json(corporateaction))) from(select security,action,date from itrader_corporateaction) corporateaction")
        action = cur.fetchone()
        action = json.dumps(action[0])
        cur.execute("select array_to_json(array_agg(row_to_json(equity))) from(select sentimentscore from itrader_news where content LIKE '%equity%') equity")
        equity = cur.fetchone()
        equity = json.dumps(equity[0])
        
        #close cursor
        cur.close()  
        return render(request, "itrader/itrader.html",  {'data': data, 'username':username, 'profile':profile,'action':action,'equity':equity})
    except:
       return('Error Connecting') 
    finally:
        #close the connection
        con.close()  