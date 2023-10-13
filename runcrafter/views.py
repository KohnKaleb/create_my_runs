from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import redirect
from Oauth.models import Activities
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.http import JsonResponse
from django import forms

class runCriteria(forms.Form):
    distance = forms.CharField()
    elevation = forms.CharField()

# Create your views here.
@csrf_exempt
def craft_runs(request):
    if request.method == 'POST':
        # encode the bottom using utf-8 
        form = runCriteria(request.POST)
        print(form)
        if form.is_valid():
            distance = form.cleaned_data['distanceSlider']
            elevation = form.cleaned_data['elevationSlider']
            distance_value = int(distance)
            meters_val = int(distance_value) * 1609.344
            elevation_value = int(elevation)
            upper_dist = meters_val + (meters_val * 0.2)
            lower_dist = meters_val - (meters_val * 0.2)
            upper_elv = elevation_value + (elevation_value * 0.2)
            lower_elv = elevation_value - (elevation_value * 0.2)

            # Use the filter() method with Q objects to specify the range condition
            results = Activities.objects.filter(Q(distance__gte=lower_dist) & Q(distance__lte=upper_dist)
                                             & Q(total_elevation_gain__gte=lower_elv) & Q(total_elevation_gain__lte=upper_elv))
        
            show = 5
            return JsonResponse({"runs": list(results.values())[:show], "csrf": request.META['CSRF_COOKIE']})
        else: 
            errors = form.errors
            return JsonResponse({'errors': errors}, status=400)  # Return validation errors