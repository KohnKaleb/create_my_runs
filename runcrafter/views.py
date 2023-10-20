from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import redirect
from Oauth.models import Activities
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.conf import settings
from django.http import JsonResponse
from django import forms
import polyline

# Create your views here.
@csrf_exempt
def craft_runs(request):
    if request.method == 'GET':
        distance = request.GET.get('distanceSlider')
        elevation = request.GET.get('elevationSlider')
        distance_value = int(distance)
        meters_val = int(distance_value) * 1609.344
        elevation_value = int(elevation) * 3.3
        upper_dist = meters_val + 10000 #(meters_val * 0.2)
        lower_dist = meters_val - 10000 #(meters_val * 0.2)
        upper_elv = elevation_value + 500 #(elevation_value * 0.2)
        lower_elv = elevation_value - 500 # (elevation_value * 0.2)
        MAPBOX_KEY = settings.MAPBOX_KEY

        # Use the filter() method with Q objects to specify the range condition
        results = Activities.objects.filter(Q(distance__gte=lower_dist) & Q(distance__lte=upper_dist)
                                             & Q(total_elevation_gain__gte=lower_elv) & Q(total_elevation_gain__lte=upper_elv))
        lines = []
        show = 5
        it_results = list(results.values())[:show]
        results = list(results.values())[:show]

        for run in it_results:
            poly = run['mappolyline']
            coords = polyline.decode(poly, geojson=True)
            coords = [list(tup) for tup in coords]
            lines.append(coords)
        lines = json.dumps(lines)
        return render(request, 'home.html', {'results': results, 'MAPBOX_KEY': MAPBOX_KEY, 'routes':True, 'lines':lines})

    else: 
        errors = request.errors
        return JsonResponse({'errors': errors}, status=400)  # Return validation errors