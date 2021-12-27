from django.urls import path
from . import views

app_name = 'itrade'
urlpatterns = [
    path('', views.index, name='index'),
]