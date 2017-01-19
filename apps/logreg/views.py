from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import requests, json, os

COMBATS_PORT = os.getenv('COMBATS_SERVICE_SERVICE_PORT', '5000')
COMBATS_HOST = os.getenv('COMBATS_SERVICE_SERVICE_HOST', 'localhost')
COMBATS_PATH = "http://" + COMBATS_HOST + ":" + COMBATS_PORT

# Create your views here.
def index(request):
    return render(request, 'logreg/index.html')


def log_in(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            request.session['id'] = user.id
            print request.session['id']
            return redirect('/siege/')
        else:
            return render(request, 'logreg/index.html', {'error': 'Disabled account'})
    else:
        return render(request, 'logreg/index.html', {'error':'Invalid user credentials!'})

def log_out(request):
    logout(request)
    return redirect('index')


@login_required(login_url='/', redirect_field_name=None)
def account(request):
    context = {}
    if request.method == "GET":
        user = request.user
        player = request.user.player
        illy_id = str(player.illyId)
        try:
            data = requests.get(COMBATS_PATH + "/player/" + illy_id + "/apikey").json()
            print data['key']
            key = data['key']
        except:
            key = "error occurred"
        context['name'] = user.username
        context['illyID'] = illy_id
        context['APIkey'] = key
        context['email'] = user.email
    return render(request, 'logreg/account.html', context)

@login_required(login_url='/', redirect_field_name=None)
def playername(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST['name']
        user.save()
        return redirect('account')
    else:
        return redirect('account')

@login_required(login_url='/', redirect_field_name=None)
def checkpassword(request):
    if request.method == "POST":
        user = request.user
        if user.check_password(request.POST['password']):
            print "password check success!"
            return HttpResponse("Password confirmed");
        else:
            return HttpResponse(status=401, reason="Incorrect password, try again");

@login_required(login_url='/', redirect_field_name=None)
def password(request):
    if request.method == "POST":
        user = request.user
        user.set_password(request.POST['password'])
        user.save()
        return redirect('account')


@login_required(login_url='/', redirect_field_name=None)
def email(request):
    if request.method == "POST":
        user = request.user
        user.email = request.POST['email']
        user.save()
        return redirect('account')

@login_required(login_url='/', redirect_field_name=None)
def apikey(request):
    if request.method == "POST":
        payload = {}
        payload['player'] = request.user.player.illyId
        payload['key'] = request.POST['key']
        req = requests.post(COMBATS_PATH+"/apikey/", data=json.dumps(payload))
        if req.status_code == 200:
            return redirect('account')
        else:
            user = request.user
            player = request.user.player
            context={}
            context['name'] = user.username
            context['illyID'] = player.illyId
            context['APIkey'] = req.reason
            context['email'] = user.email
            return render(request, 'logreg/account.html', context)


