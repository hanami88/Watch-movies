from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("changepassword", views.changepassword),
    path("update_user/<int:id>", views.update_user),
    path("user", views.user),
    path("delete_user/<int:id>", views.delete_user),
    path("update_phim/<slug:slug>", views.update_phim,name="update_phim_page"),
    path("delete_phim/<slug:slug>", views.delete_phim),
    path("addphim", views.addphim),
]
