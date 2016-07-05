from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import availRide
from .models import availRideModel
from datetime import datetime,timedelta

def home(request):
    return render(request, "home.html")


def thanks(request):
    if request.method == 'POST':
        return render(request, "twift/offerRide.html")

def ride_offer(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
          
            return HttpResponseRedirect('/thanks/')
    else:
        form = RideForm()

    return render(request, "twift/offerRide.html", {'form': form})


def avail_ride(request):
    if request.method == 'POST':
        form = availRide(request.POST)
        if form.is_valid():
            dur = form.cleaned_data["duration"]
            print(dur)
            datenew=datetime.now()+timedelta(minutes=int(dur))
            print(datenew  )
            print(datetime.now())
            newRideReq=availRideModel(uid=request.user,source=form.cleaned_data["source"],startx=form.cleaned_data["sourcex"],starty=form.cleaned_data["sourcey"],destination=form.cleaned_data["destination"],destinationx=form.cleaned_data["destinationx"],destinationy=form.cleaned_data["destinationy"],datePublished=datenew)
            print(newRideReq)
            newRideReq.save()
            print(newRideReq.datePublished)
            return HttpResponseRedirect('./thanks/')
    else:
        form = availRide()
    
    return render(request,'twift/avaiRide.html',{'form':form})