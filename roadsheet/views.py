# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Roadsheets, Tablets, Cars, Drivers, DocTabletSim, SimCards, DocQualityTablet, TabletQuality
from forms import RoadsheetForm, DocTabletSimForm, DocQualityTabletForm, DocAddTmcForm
import datetime

# Create your views here.

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def start(request):
    roadsheets = Roadsheets.objects.filter(active=True, deleted=False)
    drafts_roadsheets = Roadsheets.objects.filter(draft=True, deleted=False)
    closed_roadsheets = Roadsheets.objects.filter(active=False, closed_datetime__gt=datetime.date.today())

    context = {
        'roadsheets': roadsheets,
        'drafts_roadsheets': drafts_roadsheets,
        'closed_roadsheets': closed_roadsheets,
    }
    return render(request, 'roadsheet/index.html', context)

def roadsheet(request, sheet_id=None, Form=None):
    # Редактирование либо сохранение
    if request.method == 'POST':
        if sheet_id is None:
            form = RoadsheetForm(request.POST)
        else:
            form = RoadsheetForm(request.POST, instance=Roadsheets.objects.get(id=sheet_id))

    elif sheet_id is None:
        # Отбираем доступные планшеты, машины,
        form = RoadsheetForm()

    else:
        form = RoadsheetForm(instance=Roadsheets.objects.get(id=sheet_id))
        tmp = Roadsheets.objects.get(id=sheet_id)
        tmp.deleted = True

    if form.is_valid():
        form.save()
        return redirect(reverse('start'))

    context = {'form': form}
    cars_in_use = Roadsheets.objects.filter(active=True, deleted=False).values_list('car', flat=True)
    cars_accessible = Cars.objects.exclude(id__in=cars_in_use)
    drivers_in_use = Roadsheets.objects.filter(active=True, deleted=False).values_list('driver', flat=True)
    drivers_accessible = Drivers.objects.exclude(id__in=drivers_in_use)
    form.fields['car'].queryset = cars_accessible
    form.fields['driver'].queryset = drivers_accessible
    return render(request, 'roadsheet/add_roadsheet.html', context)

# Передача ТМЦ на рейс
def doc_add_tmc(request):
    if request.method == 'POST':
        form = DocAddTmcForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('start'))
    else:
        form = DocAddTmcForm()

    context = {'form': form}

    return render(request, 'roadsheet/doc_add_tmc.html', context)




def begin_route(request, sheet_id):
    if request.user.is_authenticated:
        road_sheet = Roadsheets.objects.get(id=sheet_id)
        if road_sheet.active == False:
            road_sheet.active = True
            road_sheet.draft = False
            road_sheet.operator = request.user.username
            road_sheet.execution_datetime = datetime.datetime.now()
            road_sheet.save()
        else:
            return HttpResponse("Рейс уже открыт")
        return redirect(reverse('start'))
    else:
        return HttpResponse("Требуется авторизация")

def delete_route(request, sheet_id):
    if request.user.is_authenticated:
        road_sheet = Roadsheets.objects.get(id=sheet_id)
        if road_sheet.active == False:
            road_sheet.deleted = True
            road_sheet.save()

        else:
            return HttpResponse("Рейс уже открыт")

        return redirect(reverse('start'))
    else:
        return HttpResponse("Требуется авторизация")


#Формирование документов
def doc_part_tablet_sim(request):
    if request.method == 'POST':
        form = DocTabletSimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('doc_part_tablet_sim'))
    else:
        form = DocTabletSimForm()

    tablets = DocTabletSim.objects.filter(aparted_timestamp=None)
    tablets_in_use = DocTabletSim.objects.filter(aparted_timestamp=None).values_list('tablet', flat=True)
    tablets_accessible = Tablets.objects.exclude(id__in=tablets_in_use)
    sim_in_use = DocTabletSim.objects.filter(aparted_timestamp=None).values_list('sim', flat=True)
    sim_accessible = SimCards.objects.exclude(id__in=sim_in_use)
    form.fields['tablet'].queryset = tablets_accessible
    form.fields['sim'].queryset = sim_accessible

    context = {'form': form, 'tablets':tablets}

    return render(request, 'roadsheet/doc_part_tablet_sim.html', context)

#Расформировываем комплект
def doc_apart_tablet_sim(request, doc_id):
    if request.method == 'GET':
        doc = DocTabletSim.objects.get(id = doc_id)
        doc.aparted_timestamp = datetime.datetime.now()
        doc.save()


        return redirect(reverse('doc_part_tablet_sim'))
    else:
        return HttpResponse("Так не надо делать")

    # Установка качества планшетов
def doc_quality_tablet(request):
    if request.method == 'POST':
        form = DocQualityTabletForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('doc_quality_tablet'))
    else:
        form = DocQualityTabletForm()

    uniquedoc = []
    tl = []
    tablets = DocQualityTablet.objects.order_by('-timestamp')
    for n in tablets:
        if n.tablet.id not in tl:
            uniquedoc.append(n.id)
            tl.append(n.tablet.id)
    tablet_filtered = tablets.filter(id__in=uniquedoc)

    form.fields['tablet'].queryset = Tablets.objects.all()
    form.fields['quality'].queryset = TabletQuality.objects.all()
    context = {'form': form, 'tablets': tablets, 'tablets_last': tablet_filtered }

    return render(request, 'roadsheet/doc_quality_tablet.html', context)



#Печать документов
def print_roadsheet(request, sheet_id):
    road_sheet = Roadsheets.objects.get(id=sheet_id)
    context = {
        's': road_sheet,
    }
    return render(request, 'roadsheet/print_roadsheet.html', context)



# Авторизация

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
    return render(request, 'roadsheet/index.html',{'username':request.user.username})

def close_route(request, sheet_id=None):
    if request.user.is_authenticated:
        if sheet_id == None:
            return HttpResponse("Не указан рейс")
        else:
            #TODO Проверка перед закрытием
            road_sheet = Roadsheets.objects.get(id=sheet_id)
            road_sheet.active = False
            road_sheet.closed_datetime = datetime.datetime.now()
            road_sheet.operator = request.user.username
            road_sheet.save()
            return redirect(reverse('start'))
    else:
        return HttpResponse("Требуется авторизация")