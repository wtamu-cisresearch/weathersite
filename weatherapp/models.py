from django.db import models

# Create your models here.
class SensorModel(models.Model):
	name = models.CharField('Model Name', max_length=200)
	description = models.CharField('Description', max_length=200)
	def __unicode__(self):
		return self.description + " (" + self.name + ")"
		
class Sensor(models.Model):
	name = models.CharField('Sensor Name', max_length=200)
	model = models.ForeignKey(SensorModel)
	address = models.CharField('IP Address or Serial Port', max_length=200)
	sample_rate = models.IntegerField('Sample rate in minutes', default=1)
	def __unicode__(self):
		return self.name
		
class DataType(models.Model):
	name = models.CharField('Name', max_length=200)
	units = models.CharField('Units', max_length=200)
	sensorlib_id = models.IntegerField('Sensorlib ID')
	def __unicode__(self):
		return self.name + " (" + self.units + ")"
		
class WeatherData(models.Model):
	sensor = models.ForeignKey(Sensor)
	type = models.ForeignKey(DataType)
	value = models.FloatField()
	timestamp = models.DateTimeField()