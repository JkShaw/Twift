from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
# Create your models here.
class UserDetails(models.Model):
	MALE = 'm'
	FEMALE = 'f'
	uid =models.ForeignKey(User)
	address=JSONField(default=list([]))
	isdriver=models.BooleanField()
	GENDER_CHOICES=(
		(MALE,'Male'),
		(FEMALE,'Female'),
		)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default=MALE)
class DriverUsers(models.Model):
	uid =models.ForeignKey(User)
	driverlicense=models.CharField(max_length=20)

class VehicleDetails(models.Model):
	vehicleregistration=models.CharField(max_length=20)
	vehiclemodel=models.CharField(max_length=20)
	milage=models.FloatField()
	owner=models.ForeignKey(User)

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
