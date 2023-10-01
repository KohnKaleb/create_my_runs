from django.shortcuts import render
from django.shortcuts import redirect
import requests
from django.conf import settings


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
        MAPBOX_KEY = settings.MAPBOX_KEY
        
        
        if response:
            return render(request, 'home.html', {'access_token': response.json(), 'MAPBOX_KEY': MAPBOX_KEY})
        

    
    return render(request, 'home.html')

def exchange_code_for_token(authorization_code):
    token_url = 'https://www.strava.com/api/v3/oauth/token'
    client_id = settings.STRAVA_CLIENT_ID
    client_secret = settings.STRAVA_CLIENT_SECRET
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
    route = 'https://www.strava.com/oauth/authorize?client_id=' + str(settings.STRAVA_CLIENT_ID) + '&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all'
    return redirect(route)