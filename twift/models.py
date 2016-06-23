from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
# Create your models here.
class user_details(models.Model):
	MALE = 'm'
	FEMALE = 'f'
	uid =models.ForeignKey(User)
	address=JSONField(default=list([]))
	isdriver=models.BooleanField()
	gender=(
		(MALE,'Male'),
		(FEMALE,'Female'),
		)

class driver_users(models.Model):
	uid =models.ForeignKey(User)
	driverlicense=models.CharField(max_length=20)

class vehicle_details(models.Model):
	vehicleregistration=models.CharField(max_length=20)
	vehiclemodel=models.CharField(max_length=20)
	milage=models.FloatField()
	owner=models.ForeignKey(User)

class journey(models.Model):
	passenger=models.ForeignKey(User,related_name='the_passsenger')
	driver=models.ForeignKey(User,related_name='the_driver')
	startx=models.FloatField()
	starty=models.FloatField()
	destinationx=models.FloatField()
	destinationy=models.FloatField()
	waypoints=JSONField(default=list([]))

class journey_feeback(models.Model):
	uid=models.ForeignKey(User)
	journeyid=models.ForeignKey(journey)
	feedback=models.CharField(max_length=100)
