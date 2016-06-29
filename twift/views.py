from django.shortcuts import render
from django.http import HttpResponseRedirect

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