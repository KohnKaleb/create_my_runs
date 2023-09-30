from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^.*exchange_token.*$', views.strava_callback, name='strava_callback')
]
