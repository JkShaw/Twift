from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import OfferRides

# If you don't do this you cannot use Bootstrap CSS


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class OfferRideForm(forms.ModelForm):
    CHOICES = (('1', '1',), ('2', '2',))
    source = forms.CharField(label="Source",
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    destination = forms.CharField(label="Destination",
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    seats = forms.ChoiceField(label="Seats Available", choices=CHOICES,
                              widget=forms.Select(attrs={'class': 'form-control selector'}))
    lat_src = forms.FloatField(required=False, widget=forms.HiddenInput())
    lng_src = forms.FloatField(required=False, widget=forms.HiddenInput())
    lat_dest = forms.FloatField(required=False, widget=forms.HiddenInput())
    lng_dest = forms.FloatField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = OfferRides
        fields = ('source',)
