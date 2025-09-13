from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
path("<slug:slug>", views.xemphim),
        path('<slug:slug>/thich', views.thich),
    path("<slug:slug>/comment", views.comment),
]
