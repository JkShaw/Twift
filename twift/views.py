from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import availRide, OfferRideForm
from .models import availRideModel, OfferRides
from datetime import datetime, timedelta


def home(request):
    return render(request, "home.html")


def thanks(request):
    if request.method == 'POST':
        return render(request, "twift/offerNewRide.html")


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


def avail_ride(request):
    if request.method == 'POST':
        form = availRide(request.POST)
        if form.is_valid():
            dur = form.cleaned_data["duration"]
            print(dur)
            datenew = datetime.now()+timedelta(minutes=int(dur))
            print(datenew)
            print(datetime.now())
            newRideReq = availRideModel(uid=request.user, source=form.cleaned_data["source"], startx=form.cleaned_data["sourcex"], starty=form.cleaned_data["sourcey"], destination=form.cleaned_data["destination"], destinationx=form.cleaned_data["destinationx"], destinationy=form.cleaned_data["destinationy"], datePublished=datenew)
            print(newRideReq)
            newRideReq.save()
            print(newRideReq.datePublished)
            return HttpResponseRedirect('./thanks/')
    else:
        form = availRide()
    
    return render(request, 'twift/avaiRide.html', {'form': form})