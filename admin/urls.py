from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("addphim_page", views.addphim_page),
    path("changepassword_page", views.changepassword_page),
    path("update_user_page", views.update_user_page),
    path("user", views.user),
    path("update_phim_page/<slug:slug>", views.update_phim_page),
    path("update_phim/<slug:slug>", views.update_phim,name="update_phim_page"),
    path("delete_phim/<slug:slug>", views.delete_phim),
    path("addphim", views.addphim),
]
