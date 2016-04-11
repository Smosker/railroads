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

    def clean(self):
        cleaned_data = super(RouteCreation, self).clean()
        departure = cleaned_data.get('departure_date')
        destination = cleaned_data.get('destination_date')

        if not (departure and destination):
            """
            Проверка на корректность введенной даты - если преобразование в дату не удалось - одно из
            значений будет None
            """
            raise forms.ValidationError("Error: you have to provide a valid date. ")

        if departure > destination:
                raise forms.ValidationError("Error: date of arrival should be after date of departure")

        return cleaned_data




