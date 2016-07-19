from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .models import AvailRideModel,OfferRides,DriverUsers
from django.utils import html


class SubmitButtonWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return '<input type="submit" name="%s" value="%s">' % (html.escape(name), html.escape(value))


class SubmitButtonField(forms.Field):
    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {}
        kwargs["widget"] = SubmitButtonWidget

        super(SubmitButtonField, self).__init__(*args, **kwargs)

    def clean(self, value):
        return value

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class AvailRide(forms.Form):
	
	source = forms.CharField(widget=forms.HiddenInput(attrs={'class': 
    'form-control', 'name': 'source'}))
	destination = forms.CharField(widget=forms.HiddenInput(attrs={'class': 
    'form-control', 'name': 'destination'}))
	lat_src = forms.CharField(widget=forms.HiddenInput(attrs={'class': 
    'form-control', 'name': 'lat_src'}))
	lng_src = forms.CharField(widget=forms.HiddenInput(attrs={'class': 
    'form-control', 'name': 'lng_src'}))
	lat_dest = forms.CharField(widget=forms.HiddenInput(attrs={'class': 
    'form-control', 'name': 'lat_dest'}))
	lng_dest = forms.CharField(widget=forms.HiddenInput(attrs={'class': 
    'form-control', 'name': 'lng_dest'}))
	duration =forms.CharField(widget=forms.HiddenInput(attrs={'class': 
    'form-control', 'name': 'duration','value':'0'}))
	class Meta:
		model = AvailRideModel
class ChooseRides(forms.Form):
  rideschoices = forms.CharField(widget=forms.HiddenInput(attrs={'class': 
    'form-control', 'name': 'rideschoices','value':'[]'})) 
  searchField = forms.CharField(widget=forms.HiddenInput(attrs={'class': 
    'form-control', 'name': 'searchField'})) 
  submit_button = SubmitButtonField(label="Choose Rides", initial=u"Choose Rides",disabled='true') 

class OfferRideForm(forms.Form):
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


class DriverDetailsForm(forms.ModelForm):
    driverlicense = forms.CharField( label="Driver License",
                                        required=True,
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DriverUsers
        fields = ('driverlicense',)
