# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Roadsheets, Tablets, Cars, Drivers, DocTabletSim, SimCards, DocQualityTablet, TabletQuality,\
    DocAddTmc, DocRequest, Organization
from forms import RoadsheetForm, DocTabletSimForm, DocQualityTabletForm, DocAddTmcForm, DocRequestForm
from django import forms
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

    repair_requests = DocRequest.objects.filter(closed_timestamp__isnull=True)


    context = {
        'roadsheets': roadsheets,
        'drafts_roadsheets': drafts_roadsheets,
        'closed_roadsheets': closed_roadsheets,
        'repair_requests' : repair_requests,

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
    if request.user.is_authenticated:
        rs = Roadsheets.objects.get(id=sheet_id)
        if rs.execution_timestamp is None and rs.closed_timestamp is None:
            rs.deleted = True
            rs.save()
            return redirect(reverse('start'))
        else:
            return HttpResponse("Рейс открыт или не существует")
    else:
        return HttpResponse("Требуется авторизация")

# Открытие рейса
def roadsheet_open(request, sheet_id):
    if request.user.is_authenticated:
        rs = Roadsheets.objects.get(id=sheet_id)
        if rs.execution_timestamp is None:
            rs.operator_open = request.user.username
            rs.execution_timestamp = datetime.datetime.now()
            rs.save()
            return redirect(reverse('start'))
        else:
            return HttpResponse("Рейс уже открыт")
    else:
        return HttpResponse("Требуется авторизация")

# Закрытие рейса
def roadsheet_close(request, sheet_id=None):
    if sheet_id == None:
        return HttpResponse("Не указан рейс")

    if request.method == 'POST':

        rs = Roadsheets.objects.get(id=sheet_id)
        rs.closed_timestamp = datetime.datetime.now()
        rs.save()
        if rs.get_tablet() is None:
            return HttpResponse("<script>window.close();window.opener.location.reload();</script>")

        dac = DocAddTmc.objects.filter(aparted_timestamp__isnull=True).get(tablet=rs.get_tablet().tablet_id)
        dac.aparted_timestamp = datetime.datetime.now()
        dac.save()
        return HttpResponse("<script>window.close();window.opener.location.reload();</script>")

    else:
        # TODO Проверка всего чего только можно перед закрытием
        rs = Roadsheets.objects.get(id=sheet_id)
        try:
            qualitis = rs.get_tablet().tablet.get_doc_quality_tablet().quality.all()
        except Exception:
            qualitis = None
        context ={'rs':rs, 'sheet_id': sheet_id, 'qualitis':qualitis}
        return render(request, 'roadsheet/roadsheet_close.html', context)





# ----------------------
#Формирование документов
# ----------------------

# Передача ТМЦ на рейс
# --------------------
# Если POST то сохраняем
# Если GET то отбор в зависимости от указанного sheet_id
def doc_add_tmc(request, sheet_id=None):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DocAddTmcForm(request.POST)
            if form.is_valid():

                newdoc = form.save(commit=False)
                try:
                    dac = DocAddTmc.objects.filter(aparted_timestamp__isnull=True).get(roadsheet_id=newdoc.roadsheet_id)
                    dac.aparted_timestamp = datetime.datetime.now()
                    dac.save()
                    form.save()
                except Exception:
                    form.save()
                return HttpResponse("<script>window.close();window.opener.location.reload();</script>")
        else:
            if sheet_id is None:
                form = DocAddTmcForm()
                # Отбор всех доступных планшетов и всех рейсов
                rs_a = Roadsheets.objects.filter(closed_timestamp__isnull=True, execution_timestamp__isnull=False)
                used_tablets = DocAddTmc.objects.filter(aparted_timestamp__isnull=True).values_list('tablet', flat=True)
                tblt_a = Tablets.objects.exclude(id__in = used_tablets)

                # TODO Надо исключить поломаные
                form.fields['roadsheet'].queryset = rs_a
                form.fields['tablet'].queryset = tblt_a
            else:
                # TODO Отбор для смены планшета
                # Отбор всех доступных планшетов и одного рейса
                # TODO Отбор для фиксированного планшета
                form = DocAddTmcForm()
                #form = DocAddTmcForm(instance=DocAddTmc.objects.get(roadsheet=sheet_id))
                rs_a = Roadsheets.objects.filter(id = sheet_id)
                used_tablets = DocAddTmc.objects.filter(aparted_timestamp__isnull=True ).values_list('tablet', flat=True)

                tblt_a = Tablets.objects.exclude(id__in=used_tablets)

                form = DocAddTmcForm(initial={'roadsheet':rs_a})
                # TODO Надо исключить поломаные
                form.fields['roadsheet'].queryset = rs_a
                form.fields['tablet'].queryset = tblt_a
                form.fields['roadsheet'].empty_label = None
                # TODO Установить значение SELECTED

            context = {'form': form}
            return render(request, 'roadsheet/doc_add_tmc.html', context)
    else:
        return HttpResponse("Требуется авторизация")

# Комплектация планшета симкой
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

# Раскомплектация планшета симкой
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

# Запрос на ремонт
def doc_create_request(request, sheet_id=None, tablet_id=None):
    if request.method == 'POST':
        # TODO Создание запроса на ремонт


        form = DocRequestForm(request.POST)
        form.save()
        return HttpResponse("<script>window.close();window.opener.location.reload();</script>")
    else:
        # TODO формирование запроса на основе путевого листа

        form = DocRequestForm()

        rs = Roadsheets.objects.get(id=sheet_id)
        qualities = rs.get_tablet().tablet.get_doc_quality_tablet().quality.all()

        form.fields['tablet'].queryset = Tablets.objects.filter(id=tablet_id)
        form.fields['tablet'].empty_label = None
        form.fields['roadsheet'].queryset = Roadsheets.objects.filter(id=sheet_id)
        form.fields['roadsheet'].empty_label = None
        form.fields['tablet_break_request'].widget = forms.SelectMultiple(attrs={'size': '8'})
        form.fields['tablet_break_request'].queryset = TabletQuality.objects.all()

        context ={'rs':rs, 'sheet_id': sheet_id, 'qualities':qualities, 'form':form, 'request':request}
        return render(request, 'roadsheet/doc_create_request.html', context)
    pass

# Печатные формы
# --------------
#Печать документов
def print_roadsheet(request, sheet_id):
    road_sheet = Roadsheets.objects.get(id=sheet_id)
    organization = Organization.objects.get()
    categories = road_sheet.driver.license_category.all()
    now = datetime.datetime.now()
    context = {
        's': road_sheet,
        'org': organization,
        'cats': categories,
        'now':now
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
    if request.method == 'POST':
        print request

        logout(request)
        return HttpResponse("<script>window.close();window.opener.location.reload();</script>")
    else:
        if not request.user.has_perm('roadsheet.add_car'):
            used_tablets = DocAddTmc.objects.filter(aparted_timestamp__isnull=True).values_list('tablet', flat=True)
            tblt_a = Tablets.objects.exclude(id__in=used_tablets)
            used_tablets = Tablets.objects.filter(id__in=used_tablets)
            context = {'used_tablets':used_tablets, 'tblt_a':tblt_a}
            return render(request, 'roadsheet/doc_end_day.html', context)
        else:
            logout(request)
            return HttpResponse("<script>window.close();window.opener.location.reload();</script>")



