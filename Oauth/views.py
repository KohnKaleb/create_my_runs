from django.shortcuts import render
from django.shortcuts import redirect
import requests
import polyline
import json
from django.conf import settings
from .models import Activities

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

        response = requests.get(url, headers=headers).json()
        MAPBOX_KEY = settings.MAPBOX_KEY
        
        if response:
            for activity in response:
                if activity['map'] == None or activity['map']['summary_polyline'] == None:
                    continue
                add_to_db(activity)
            activity['map']['summary_polyline'] = polyline.decode(activity['map']['summary_polyline'], geojson=True)
            activity['map']['summary_polyline'] = [list(tup) for tup in activity['map']['summary_polyline']]
            poly = response[0]['map']['summary_polyline']
            coords = polyline.decode(poly, geojson=True)
            coords = [list(tup) for tup in coords]
            return render(request, 'home.html', {'access_token': response, 'MAPBOX_KEY': MAPBOX_KEY, 'poly': poly, 'coords': coords})
        
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


def add_to_db(activity):
    if not Activities.objects.filter(athlete_id=activity["athlete"]["id"], activity_id=activity["id"]).exists():
            entry = Activities(athlete_id=activity["athlete"]["id"], activity_id=activity["id"], name=activity["name"], distance=activity["distance"], total_elevation_gain=activity["total_elevation_gain"], type=activity["type"], location_city=activity["location_city"], location_state=activity["location_state"], location_country=activity["location_country"], mapid=activity["map"]["id"], mappolyline=activity["map"]["summary_polyline"], mapresource_state=activity["map"]["resource_state"], upload_id=activity["upload_id"])
            entry.save()
    else:
        pass