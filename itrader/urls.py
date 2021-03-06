from django.urls import path
from . import views

app_name = 'itrader'
urlpatterns = [
    path('home', views.home, name='home'),
    path('itrader', views.itrader, name='itrader'),
    path('contactus', views.contactus, name='contactus'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('buysell', views.buysell, name='buysell'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('news', views.news, name='news'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('itrader/chat', views.chat, name='chat'),
    path('itrader/<str:roomname>/', views.room, name='room'),
]