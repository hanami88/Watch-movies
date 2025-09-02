from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.get_home),
    path('loginpage', views.login_page),
    path('login', views.login),
    path('registerpage', views.register_page),
    path('register', views.register),
    path("logout", views.logout),
]
