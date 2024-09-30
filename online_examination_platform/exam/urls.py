from django.contrib import admin
from django.urls import path
from . import views

app_name = 'exam'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('logout', views.logoutUser, name='logoutUser'),
]
