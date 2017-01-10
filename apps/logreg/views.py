from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Player


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
        context['name'] = user.username
        context['illyID'] = player.illyId
        context['APIkey'] = "not implemented yet"
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
    pass
