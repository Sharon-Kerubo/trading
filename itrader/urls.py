from django.urls import path
from . import views

app_name = 'itrader'
urlpatterns = [
    path('', views.home, name='home'),
    path('itrader', views.itrader, name='itrader'),
    path('contactus', views.contactus, name='contactus'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]