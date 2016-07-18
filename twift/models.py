from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from datetime import datetime 
from . import constants


class UserDetails(models.Model):
    uid =models.ForeignKey(User)
    address=JSONField(default=list([]))
    isdriver=models.BooleanField()  
    gender = models.CharField(max_length=1, choices=constants.GENDER_CHOICES,default=constants.MALE)


class DriverUsers(models.Model):
    uid =models.ForeignKey(User)
    driverlicense=models.CharField(max_length=20)

    def __str__(self):
        return self.driverlicense


class VehicleDetails(models.Model):
    vehicleregistration=models.CharField(max_length=20)
    vehiclemodel=models.CharField(max_length=20)
    milage=models.FloatField()
    owner=models.ForeignKey(User)

    def __str__(self):
        return self.vehicleregistration


class Journey(models.Model):
    passenger=models.ForeignKey(User,related_name='the_passsenger')
    driver=models.ForeignKey(User,related_name='the_driver')
    startx=models.FloatField()
    starty=models.FloatField()
    destinationx=models.FloatField()
    destinationy=models.FloatField()
    waypoints=JSONField(default=list([]))


class JourneyFeedback(models.Model):
    uid=models.ForeignKey(User)
    journeyid=models.ForeignKey(Journey)
    feedback=models.CharField(max_length=100)


class OfferRides(models.Model):
    user = models.ForeignKey(DriverUsers)
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    lat_src = models.FloatField()
    lng_src = models.FloatField()
    lat_dest = models.FloatField()
    lng_dest = models.FloatField()
    seats = models.IntegerField()
    datePublished = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return unicode(self.source)


class availRideModel(models.Model):
    uid=models.ForeignKey(User)
    source=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    startx=models.FloatField()
    starty=models.FloatField()
    destinationx=models.FloatField()
    destinationy=models.FloatField()
    datePublished = models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return self.source