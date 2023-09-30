from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.login),
    path('strava_redirect/', views.strava_redirect, name='strava_redirect'),
    path('strava/callback/', include('strava_api.urls'), name='strava_callback'),
    re_path(r'^.*exchange_token.*$', views.strava_callback, name='strava_callback')
]
