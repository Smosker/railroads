# coding=utf-8
from django import forms
from .models import Schedule


class RouteCreation(forms.ModelForm):
    """
    Форма отвечающая за внесение изменения в существующий
    маршрут или создание нового
    """
    class Meta:
        model = Schedule

        fields = ('train',
                  'departure_city',
                  'departure_date',
                  'destination_city',
                  'destination_date')





