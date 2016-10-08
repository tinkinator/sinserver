from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
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
