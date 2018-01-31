# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from models import Roadsheets, DocTabletSim, DocQualityTablet, DocAddTmc, DocRequest
from django.contrib.auth import authenticate


class RoadsheetForm(ModelForm):
    class Meta:
        model = Roadsheets
        fields = '__all__'
        labels = {
            "driver": "Водитель",
            "car":"Автомобиль",
            "workload": "График",
        }

class DocTabletSimForm(ModelForm):
    class Meta:
        model = DocTabletSim
        fields = '__all__'
        labels = {

        }

class DocQualityTabletForm(ModelForm):
    class Meta:
        model = DocQualityTablet
        fields = '__all__'
        labels = {

        }

class DocAddTmcForm(ModelForm):
    class Meta:
        model = DocAddTmc
        fields = '__all__'
        labels = {
            "tablet": "Планшет",
            "roadsheet": "Рейс",
        }


class DocRequestForm(ModelForm):
    class Meta:
        model = DocRequest
        fields = '__all__'
        labels = {
            "tablet": "Планшет",
            "roadsheet": "Рейс",
        }
