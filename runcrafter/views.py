from django.shortcuts import render
from django.shortcuts import redirect
from Oauth.models import Activities
import requests

# Create your views here.
def craft_runs(request):
    if request.method == 'POST':
        distance_value = request.POST.get('distanceValue')
        elevation_value = request.POST.get('elevationValue')

    return render(request, 'runs_list.html')