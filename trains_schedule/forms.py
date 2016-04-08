# coding=utf-8
from django.core.exceptions import ValidationError
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

    def clean(self):
        if self.departure_date > self.destination_date:
                raise ValidationError("Error: date of arrival should be after date of departure")





