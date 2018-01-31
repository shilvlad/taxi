# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Roadsheets, Tablets, Cars, Drivers, DocTabletSim, SimCards, DocQualityTablet, TabletQuality,\
    DocAddTmc
from forms import RoadsheetForm, DocTabletSimForm, DocQualityTabletForm, DocAddTmcForm
import datetime

# Create your views here.

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Главная вьюшка
def start(request):

    drafts_roadsheets = Roadsheets.objects.filter(execution_timestamp__isnull=True, deleted=False)
    roadsheets = Roadsheets.objects.filter(execution_timestamp__isnull=False, closed_timestamp__isnull= True, deleted=False)
    closed_roadsheets = Roadsheets.objects.filter(closed_timestamp__gt=datetime.date.today())

    used_tablets = DocAddTmc.objects.filter(aparted_timestamp__isnull=True)
    print closed_roadsheets
    print used_tablets

    doc_add_tmc_form = DocAddTmcForm()

    context = {
        'roadsheets': roadsheets,
        'drafts_roadsheets': drafts_roadsheets,
        'closed_roadsheets': closed_roadsheets,
        'doc_add_tmc_form': doc_add_tmc_form,
    }
    return render(request, 'roadsheet/index.html', context)



# Добавление редактирование рейса
# Создание черновика (Creation_timestamp) -> активация рейса (execution_timestamp) -> Закрытие рейса (clothed_timestamp)
# -------------------------------
# Возможны варианты:
# 1) Создание нового черновика рейса
# 2) Редактирование черновика
# 3) Сохранение формы
def roadsheet(request, sheet_id=None):
    # Редактирование либо сохранение
    context ={}
    if request.method == 'POST':

        form = RoadsheetForm(request.POST)
        if form.is_valid():
            form.save()
            if sheet_id is not None:
                print "DELETE "
                tmp = Roadsheets.objects.get(id=sheet_id)
                tmp.deleted = True
                tmp.save()
            #return redirect(reverse('start'))
            return HttpResponse("<script>window.close();window.opener.location.reload();</script>")
    else:

        if sheet_id is None:

            form = RoadsheetForm()
            drivers_in_use = Roadsheets.objects.filter(closed_timestamp__isnull=True, deleted=False).values_list(
                'driver', flat=True)
            drivers_accessible = Drivers.objects.exclude(id__in=drivers_in_use)
            cars_in_use = Roadsheets.objects.filter(closed_timestamp__isnull=True, deleted=False).values_list('car',
                                                                                                              flat=True)
            cars_accessible = Cars.objects.exclude(id__in=cars_in_use)

            form.fields['car'].queryset = cars_accessible
            form.fields['driver'].queryset = drivers_accessible

        else:

            form = RoadsheetForm(instance=Roadsheets.objects.get(id=sheet_id))

            drivers_in_use = Roadsheets.objects.filter(closed_timestamp__isnull=True, deleted=False).\
                exclude(id=sheet_id).values_list('driver', flat=True)
            drivers_accessible = Drivers.objects.exclude(id__in=drivers_in_use)

            cars_in_use = Roadsheets.objects.filter(closed_timestamp__isnull=True, deleted=False). \
                exclude(id=sheet_id).values_list('car', flat=True)
            cars_accessible = Cars.objects.exclude(id__in=cars_in_use)

            form.fields['car'].queryset = cars_accessible
            form.fields['driver'].queryset = drivers_accessible
            context['sheet_id'] = sheet_id

        context['form'] = form

        return render(request, 'roadsheet/roadsheet.html', context)

# Удаление рейса (только для неоткрытых рейсов)
def roadsheet_delete(request, sheet_id):
    # TODO Переделать удаление черновика маршрута к ебеням!
    if request.user.is_authenticated:
        rs = Roadsheets.objects.get(id=sheet_id)
        if rs.execution_timestamp is None and rs.closed_timestamp is None:
            rs.deleted = True
            rs.save()
            return redirect(reverse('start'))
        else:
            return HttpResponse("Ой, гонево какое!")


    else:
        return HttpResponse("Требуется авторизация")

# Открытие рейса
def roadsheet_open(request, sheet_id):
    # TODO Переделать открытие маршрута к ебеням!
    if request.user.is_authenticated:
        road_sheet = Roadsheets.objects.get(id=sheet_id)
        road_sheet.operator_open = request.user.username
        road_sheet.execution_timestamp = datetime.datetime.now()
        road_sheet.save()

        return redirect(reverse('start'))
    else:
        return HttpResponse("Требуется авторизация")

# закрытие рейса
def roadsheet_close(request, sheet_id=None):
    if request.user.is_authenticated:
        if sheet_id == None:
            return HttpResponse("Не указан рейс")
        else:
            # TODO Проверка перед закрытием
            road_sheet = Roadsheets.objects.get(id=sheet_id)
            road_sheet.closed_timestamp = datetime.datetime.now()
            road_sheet.operator_close = request.user.username
            road_sheet.save()
            return redirect(reverse('start'))
    else:
        return HttpResponse("Требуется авторизация")

# Передача ТМЦ на рейс
def doc_add_tmc(request):
    if request.method == 'POST':
        form = DocAddTmcForm(request.POST)
        if form.is_valid():
            form.save()

            context = {'form':form}

            # return render(request, 'roadsheet/doc_add_tmc.html', context)
            return redirect(reverse('start'))
    else:
        return redirect(reverse('start'))

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

