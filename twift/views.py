from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import OfferRideForm
from .models import OfferRides
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse


def home(request):
    return render(request, "home.html")


def thanks(request):
    if request.method == 'POST':
        return render(request, "twift/offerRide.html")


def offer_ride(request):
    if request.method == 'POST':
        form = OfferRideForm(request.POST)
        if form.is_valid():
            user_id = request.user.pk
            print user_id
            data = form.cleaned_data
            print(data)
            data['user_id'] = user_id
            try:
                OfferRides.objects.create(**data)
                return render_to_response('home.html')
            except Exception as e:
                print(data)
                print(str(e))
                return HttpResponseRedirect(reverse('home'))
    else:
        form = OfferRideForm()
    return render(request, "twift/offerNewRide.html", {'form': form})