from django import forms
from .models import Schedule


class RouteCreation(forms.ModelForm):
    class Meta:
        model = Schedule

        fields = ('train',
                  'departure_city',
                  'departure_date',
                  'destination_city',
                  'destination_date')





