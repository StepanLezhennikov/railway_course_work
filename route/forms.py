from django import forms
from .models import Route


class SearchForm(forms.ModelForm):
    travel_date = forms.DateField(widget=forms.SelectDateWidget, label='Дата поездки')

    class Meta:
        model = Route
        fields = ['from_station', 'to_station']
