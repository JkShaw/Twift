
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .forms import AvailRide, OfferRideForm, ChooseRides, DriverDetailsForm
from .models import AvailRideModel, OfferRides, DriverUsers, AvailToOffer
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import logging
import json

from django.core.serializers.json import DjangoJSONEncoder

from django.core import serializers
log = logging.getLogger(__name__)


def home(request):
    """Home page."""
    return render(request, "home.html")


def thanks(request):
    """Thank page."""
    if request.method == 'POST':
        return render(request, "twift/offerNewRide.html")


def get_customers(request):
    """Get customers who wants ride."""
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
            customers = (AvailRideModel.objects.select_related().filter(
                source=unicode(source),
                destination=unicode(destination)).order_by(
                    '-date_published').values(
                        'uid', 'source', 'destination', 'date_published',
                        'uid__first_name', 'uid__last_name'))
            print('Inside get customers')
            print(customers)
        else:
            customers = (AvailRideModel.objects.select_related().values(
                'uid', 'source', 'destination', 'date_published',
                'uid__first_name', 'uid__last_name'))
            print('Inside get customers')
            print(customers)
        try:
            json_customers = json.dumps(list(customers), cls=DjangoJSONEncoder)
        except Exception as e:
            print('Inside exception')
            print(str(e))
        print(json_customers)
    return HttpResponse(json_customers)


def driver_details(request):
    """Get users driver related information and redirect to offer ride page."""
    if request.method == 'POST':
        form = DriverDetailsForm(request.POST)
        if form.is_valid():
            user_id = request.user.pk
            data = form.cleaned_data
            data['user_id'] = user_id
            try:
                DriverUsers.objects.create(**data)
                return HttpResponseRedirect(reverse('offer_ride'))
            except Exception as e:
                print(str(e))
                return HttpResponseRedirect(reverse('offer_ride'))
    else:
        form = DriverDetailsForm()
    return render(request, "twift/getDriverDetails.html", {'form': form})


def offer_ride(request):
    """Offer ride page."""
    if request.method == 'POST':
        form = OfferRideForm(request.POST)
        if form.is_valid():
            du = DriverUsers.objects.filter(user=request.user)
            print(du[0].user_id)
            data = form.cleaned_data
            print(data)
            data['user'] = du[0]

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
            user_id=request.user.pk).exists()
        if not driver_exists:
            # Set driver details
            form = DriverDetailsForm()
            return HttpResponseRedirect("../getDriverDetails")
        else:
            form = OfferRideForm()
            return render(request, "twift/offerNewRide.html", {'form': form})


@login_required
def avail_ride(request):
    """Set customers information who wants ride."""
    if request.method == 'POST':
        form = AvailRide(request.POST)
        if form.is_valid():

            try:
                dur = form.cleaned_data["duration"]
                log.info(dur)
                datenew = datetime.now() + timedelta(minutes=int(dur))
                log.info(datenew)
                log.info(datetime.now())
                newridereq = AvailRideModel(
                    uid=request.user,
                    source=form.cleaned_data["source"],
                    lat_src=form.cleaned_data["lat_src"],
                    lng_src=form.cleaned_data["lng_src"],
                    destination=form.cleaned_data["destination"],
                    lat_dest=form.cleaned_data["lat_dest"],
                    lng_dest=form.cleaned_data["lng_dest"],
                    date_published=datenew)
                log.info(form.cleaned_data)
                serialized_obj = serializers.serialize('json', [newridereq, ])
                # newridereq.save()
                log.info(newridereq.date_published)
                ride_offers = OfferRides.objects.select_related()
                print(ride_offers)
                form1 = ChooseRides(
                    {
                        'searchField': serialized_obj,
                        'rideschoices': '[]',
                        'submit_button': 'Choose Rides and Submit'})
                return render(
                    request,
                    'twift/avaiRide.html',
                    {
                        'form': form,
                        'ride_offers': ride_offers,
                        'form1': form1})
            except Exception as e:
                log.error(newridereq)
                log.error(e)
                return HttpResponseRedirect(reverse('home'))

    else:
        form = AvailRide()

    return render(request, 'twift/avaiRide.html', {'form': form})


def show_available_rides(request):
    """Show available rides."""
    if request.method == 'POST':
        form = ChooseRides(request.POST)
        if form.is_valid():
            log.info(form.cleaned_data)
            rideavailed = json.loads(form.cleaned_data["rideschoices"])
            searchField = json.loads(form.cleaned_data["searchField"])
            newridereq = AvailRideModel(
                uid=request.user,
                source=searchField[0]['fields']['source'],
                lat_src=searchField[0]['fields']["lat_src"],
                lng_src=searchField[0]['fields']["lng_src"],
                destination=searchField[0]['fields']["destination"],
                lat_dest=searchField[0]['fields']["lat_dest"],
                lng_dest=searchField[0]['fields']["lng_dest"],
                date_published=searchField[0]['fields']['date_published'])
            newridereq.save()
            for value in rideavailed:
                log.info(value)
                avail = newridereq
                offer = OfferRides.objects.filter(
                    id=int(value['driver_ride_id']))[0]
                newatoo = AvailToOffer(avail=avail, offer=offer)
                newatoo.save()

            return render(request, "home.html")
    ride_offers = OfferRides.objects.all()
    print(ride_offers.count())
    return render(
        request, 'twift/rideOffers.html',
        {'ride_offers': ride_offers})
