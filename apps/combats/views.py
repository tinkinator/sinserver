from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import requests
from urlparse import urljoin


# Create your views here.
COMBATS_PATH = os.getenv('COMBATS_PATH', 'http://localhost:5000/')


def health(request):
    r = requests.get(COMBATS_PATH)
    data = r.json()
    response = json.dumps(data)
    return HttpResponse(response, content_type='application/json')