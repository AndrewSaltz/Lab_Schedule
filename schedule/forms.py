from schedule.models import Event, period_choices, cart_choice
from django.forms import ModelForm
from django.forms import modelformset_factory
from django import forms


class ReservationForm(ModelForm):
    class Meta:
        model = Event
        fields = ('teacher', 'is_reserved',)


#ReservationFormset = modelformset_factory(Event, fields=('day', 'teacher', 'is_reserved', 'period', 'cart'),
                                    #      widgets={'teacher': forms.HiddenInput(), 'is_reserved': forms.HiddenInput()})
