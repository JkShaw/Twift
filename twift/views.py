import json
from datetime import datetime, timedelta

from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, render_to_response


from .forms import DriverDetailsForm, OfferRideForm, availRide
from .models import DriverUsers, OfferRides, availRideModel


def home(request):
    return render(request, "home.html")


def thanks(request):
    if request.method == 'POST':
        return render(request, "twift/offerNewRide.html")


def get_customers(request):
    source = None
    destination = None
    customers = None
    if request.method == 'GET':
        source = request.GET['source']
        print(source)
        destination = request.GET['destination']
        print(destination)
        if source and destination:
            print("hello")
            customers = (availRideModel.objects.select_related().filter(
                source=unicode(source),
                destination=unicode(destination)).order_by(
                    '-datePublished').values(
                        'uid', 'source', 'destination', 'datePublished',
                        'uid__first_name', 'uid__last_name'))
            print(customers)
        else:
            customers = (availRideModel.objects.select_related().values(
                'uid', 'source', 'destination', 'datePublished',
                'uid__first_name', 'uid__last_name'))
        json_customers = json.dumps(list(customers), cls=DjangoJSONEncoder)
    return HttpResponse(json_customers)


def driver_details(request):
    if request.method == 'POST':
        form = DriverDetailsForm(request.POST)
        if form.is_valid():
            uid_id = request.user.pk
            data = form.cleaned_data
            data['uid_id'] = uid_id
            try:
                DriverUsers.objects.create(**data)
                return HttpResponseRedirect(reverse('offer_ride'))
            except Exception, e:
                print(data)
                print(str(e))
                return HttpResponseRedirect(reverse('offer_ride'))
    else:
        form = DriverDetailsForm()
    return render(request, "twift/getDriverDetails.html", {'form': form})


def offer_ride(request):
    if request.method == 'POST':
        form = OfferRideForm(request.POST)
        if form.is_valid():
            user_id = request.user.pk
            data = form.cleaned_data
            data['user_id'] = user_id
            try:
                OfferRides.objects.create(**data)
                return render_to_response('home.html')
            except Exception as e:
                print(data)
                print(str(e))
                return HttpResponseRedirect(reverse('home'))
    else:
        # See if driver registered
        driver_exists = DriverUsers.objects.filter(
            uid_id=request.user.pk).exists()
        if not driver_exists:
            # Set driver details
            form = DriverDetailsForm()
            return HttpResponseRedirect("../getDriverDetails")
        else:
            form = OfferRideForm()
            return render(request, "twift/offerNewRide.html", {'form': form})


def avail_ride(request):
    if request.method == 'POST':
        form = availRide(request.POST)
        if form.is_valid():
            dur = form.cleaned_data["duration"]
            print(dur)
            datenew = datetime.now() + timedelta(minutes=int(dur))
            print(datenew)
            print(datetime.now())
            newride_req = availRideModel(
                uid=request.user, source=form.cleaned_data["source"],
                startx=form.cleaned_data["sourcex"],
                starty=form.cleaned_data["sourcey"],
                destination=form.cleaned_data["destination"],
                destinationx=form.cleaned_data["destinationx"],
                destinationy=form.cleaned_data["destinationy"],
                datePublished=datenew)
            print(newride_req)
            newride_req.save()
            print(newride_req.datePublished)
            return HttpResponseRedirect('./thanks/')
    else:
        form = availRide()
    return render(request, 'twift/avaiRide.html', {'form': form})
