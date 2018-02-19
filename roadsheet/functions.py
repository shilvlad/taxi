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


def get_tablets_in_use():
    a = Tablets.objects.filter(id__in=DocAddTmc.objects.
        filter(aparted_timestamp__isnull=True).\
        values_list('tablet', flat=True))
    #print a
    return a


def get_tablets_in_sc():
    a = Tablets.objects.filter(id__in=DocRequest.objects.\
        filter(timestamp_in_service__isnull=False, closed_timestamp__isnull=True).\
        values_list('tablet', flat=True))
    #print a
    return a


def get_tablets_in_diagnostic():
    a = Tablets.objects.filter(id__in=DocRequest.objects.\
        filter(closed_timestamp__isnull=True, timestamp_in_service__isnull=True).\
        values_list('tablet', flat=True))
    #print a
    return a


def get_tablets_accessible():
    # In use
    a = Tablets.objects.filter(id__in=DocAddTmc.objects.
                               filter(aparted_timestamp__isnull=True). \
                               values_list('tablet', flat=True))
    #print a
    # In sc
    b = Tablets.objects.filter(id__in=DocRequest.objects. \
                               filter(timestamp_in_service__isnull=False, closed_timestamp__isnull=True). \
                               values_list('tablet', flat=True))
    #print b
    # In diagnostic
    c = Tablets.objects.filter(id__in=DocRequest.objects. \
                               filter(closed_timestamp__isnull=True, timestamp_in_service__isnull=True). \
                               values_list('tablet', flat=True))
    #print c

    d = Tablets.objects.exclude(id__in=a.values_list('id', flat=True)).\
            exclude(id__in=b.values_list('id', flat=True)).\
            exclude(id__in=c.values_list('id', flat=True))
    #print d
    return d





