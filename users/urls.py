from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("information", views.information),
    path("save", views.save),
]
