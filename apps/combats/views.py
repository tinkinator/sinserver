from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import requests
from urlparse import urljoin


# Create your views here.
COMBATS_PORT = os.getenv('COMBATS_SERVICE_SERVICE_PORT', '5000')
COMBATS_HOST = os.getenv('COMBATS_SERVICE_SERVICE_HOST', 'localhost')
COMBATS_PATH = "http://" + COMBATS_HOST + ":" + COMBATS_PORT

def health(request):
    r = requests.get(COMBATS_PATH)
    data = r.json()
    response = json.dumps(data)
    return HttpResponse(response, content_type='application/json')