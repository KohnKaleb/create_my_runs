from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('craft_my_runs/', views.craft_runs),
]