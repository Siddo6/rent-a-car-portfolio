from django import forms
from .models import Car, reservation
from django.core.exceptions import ValidationError
from django_flatpickr.widgets import DatePickerInput



class ReservationForm(forms.ModelForm):
    class Meta:
        model = reservation
        fields = ['car', 'from_date', 'to_date', 'note']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.all()
        