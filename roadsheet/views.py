from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .models import Roadsheets

# Create your views here.

def start(request):
    roadsheets = Roadsheets.objects.filter(active=True)
    context = {'roadsheets': roadsheets}
    return render(request, 'roadsheet/index.html', context)

def create_routesheet():
    context = {}
    return render(request, 'roadsheet/add_routesheet.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

def user_logout(request):
    logout(request)
    return render(request, 'Portal/index.html',{'username':request.user.username})