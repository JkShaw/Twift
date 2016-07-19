
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import AvailRide, OfferRideForm,ChooseRides,DriverDetailsForm
from .models import AvailRideModel, OfferRides,DriverUsers,AvailToOffer
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import logging
import json
from datetime import datetime, timedelta

from django.core.serializers.json import DjangoJSONEncoder

from django.core import serializers
log = logging.getLogger(__name__)



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
            du = DriverUsers.objects.filter(user=request.user)
            print(du[0].user_id)
            data = form.cleaned_data
            print(data)
            data['user'] = du[0]

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

@login_required
def avail_ride(request):
  
    if request.method == 'POST':
        form = AvailRide(request.POST)
        if form.is_valid():

            try:
                dur = form.cleaned_data["duration"]
                log.info(dur)
                datenew = datetime.now()+timedelta(minutes=int(dur))
                log.info(datenew)
                log.info(datetime.now())
                newRideReq = AvailRideModel(uid=request.user,
                 source=form.cleaned_data["source"], 
                 lat_src=form.cleaned_data["lat_src"], 
                 lng_src=form.cleaned_data["lng_src"],
                 destination=form.cleaned_data["destination"],
                 lat_dest=form.cleaned_data["lat_dest"], 
                 lng_dest=form.cleaned_data["lng_dest"], 
                 date_published=datenew)
                log.info(form.cleaned_data)
                serialized_obj = serializers.serialize('json', [ newRideReq, ])
                #newRideReq.save()
                log.info(newRideReq.date_published)
                ride_offers=OfferRides.objects.select_related();
                form1=ChooseRides({'searchField':serialized_obj,'rideschoices':'[]','submit_button':'Choose Rides and Submit'})
                return render(request, 'twift/avaiRide.html', {'form': form,
                    'ride_offers': ride_offers,'form1':form1})
            except Exception as e:
                log.error(newRideReq)
                log.error(e)
                return HttpResponseRedirect(reverse('home'))

    else:
        form = AvailRide()
    
    return render(request, 'twift/avaiRide.html', {'form': form})

def show_available_rides(request):
    if request.method == 'POST':
        form=ChooseRides(request.POST)
        if form.is_valid():
            log.info(form.cleaned_data)
            rideavailed=json.loads(form.cleaned_data["rideschoices"])
            searchField=json.loads(form.cleaned_data["searchField"])
            newRideReq=AvailRideModel(uid=request.user,
                source= searchField[0]['fields']['source'],
                lat_src=searchField[0]['fields']["lat_src"], 
                lng_src=searchField[0]['fields']["lng_src"],
                destination=searchField[0]['fields']["destination"],
                lat_dest=searchField[0]['fields']["lat_dest"], 
                lng_dest=searchField[0]['fields']["lng_dest"], 
                date_published=searchField[0]['fields']['date_published'])
            newRideReq.save();
            for value in rideavailed:
                log.info(value)
                avail=newRideReq
                offer=OfferRides.objects.filter(id=int(value['driver_ride_id']))[0]
                newAtoO=AvailToOffer(avail=avail,offer=offer);
                newAtoO.save()
                
            return render(request, "home.html")
    ride_offers=OfferRides.objects.all()
    print(ride_offers.count())
    return render(request, 'twift/rideOffers.html', {'ride_offers': ride_offers})
