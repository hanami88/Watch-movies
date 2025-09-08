from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("thich", views.thich),
    path("<slug:slug>/comment", views.comment),
    path("<slug:slug>", views.xemphim),
]
