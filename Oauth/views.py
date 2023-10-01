from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests


def login(request):
    return render(request, 'login.html')

def strava_callback(request, path=''):
    code = request.GET.get('code')
    
    if code:
        access_token = exchange_code_for_token(code)
        
        token = access_token["access_token"]
        
        url = "https://www.strava.com/api/v3/athlete/activities"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(url, headers=headers)
        
        mapbox_access_token = 'pk.eyJ1IjoibWRrdWhuIiwiYSI6ImNsbjNncmtkdTBmMzAycmw3bzUycGNhdG4ifQ.7E2AdId7t39M9-toFxsuKg'
        
        if access_token:
            return render(request, 'home.html', {'access_token': response.json()})
        

    
    return render(request, 'home.html', {'access_token': mapbox_access_token})

def exchange_code_for_token(authorization_code):
    token_url = 'https://www.strava.com/api/v3/oauth/token'
    client_id = '114433'
    client_secret = 'a4cbbad510435e4dd6c5080c486de828fb7e7752'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'grant_type': 'authorization_code'
    }
    res = requests.post(token_url, data=payload)
    
    if res.status_code == 200:
        access_token = res.json()
        return access_token
    else:
        return None

def strava_redirect(request):
    return redirect('https://www.strava.com/oauth/authorize?client_id=114433&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all')