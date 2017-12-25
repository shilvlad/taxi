from django import forms
from django.forms import ModelForm

from models import Roadsheets
from django.contrib.auth import authenticate


class RoadsheetForm(ModelForm):
    class Meta:
        model = Roadsheets
        fields = '__all__'