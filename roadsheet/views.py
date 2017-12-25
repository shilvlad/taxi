# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .models import Roadsheets
from forms import RoadsheetForm

# Create your views here.

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def start(request):
    roadsheets = Roadsheets.objects.filter(active=True)
    drafts_roadsheets = Roadsheets.objects.filter(draft=True)
    context = {'roadsheets': roadsheets, 'drafts_roadsheets':drafts_roadsheets}
    return render(request, 'roadsheet/index.html', context)

def create_roadsheet(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = RoadsheetForm(request.POST)
            if form.is_valid():
                form.operator = request.user.username
                form.save()
                return redirect(reverse('start'))
            else:
                return HttpResponse("Форма не валидна")
        else:
            form = RoadsheetForm()
            context = {'form':form}
            return render(request, 'roadsheet/add_roadsheet.html', context)
    else:
        return HttpResponse("Залогинься!")

def print_roadsheet(request, sheet_id):
    road_sheet = Roadsheets.objects.get(id=sheet_id)
    context = {
        's':road_sheet,
    }
    return render(request, 'roadsheet/print_roadsheet.html', context)

def begin_route(request, sheet_id):
    road_sheet = Roadsheets.objects.get(id=sheet_id)
    if road_sheet.active == False:
        road_sheet.active = True
        road_sheet.draft = False
        road_sheet.save()

    else:
        return HttpResponse("Рейс уже открыт")

    return redirect(reverse('start'))



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

