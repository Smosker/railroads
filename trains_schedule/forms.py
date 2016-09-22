# coding=utf-8
from django import forms
from trains_schedule.models import Schedule


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
        cleaned_data = super(RouteCreation, self).clean()
        departure = cleaned_data.get('departure_date')
        destination = cleaned_data.get('destination_date')

        if departure and destination and departure > destination:
                raise forms.ValidationError("Error: date of arrival should be after date of departure")

        return cleaned_data




