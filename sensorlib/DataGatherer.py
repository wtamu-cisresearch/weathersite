from SensorBase import SensorBase
from NullSensor import NullSensor
from USBWeatherBoard import USBWeatherBoard
from YahooWeather import YahooWeather
from weatherapp.models import Sensor, DataType, WeatherData, SensorModel
import time
import logging

class DataGatherer(object):
	# sampleRate: time in seconds between data samples
	# numberOfSamples: number of samples to gather. Set to 0 to sample indefinitely
	def __init__(self, sampleRate, numberOfSamples, myLogger):
		self.logger = myLogger
		self.sensors = []
		self.sampleRate = sampleRate
		self.numberOfSamples = numberOfSamples
		for sensor in Sensor.objects.all():
			s = None
			if (sensor.model.name == "NullSensor"):
				s = NullSensor(sensor)
			elif (sensor.model.name == "USBWeatherBoard"):
				s = USBWeatherBoard(sensor)
			elif (sensor.model.name == "YahooWeather"):
				s = YahooWeather(sensor)
			
			if (s):
				self.sensors.append(s)
#				self.logger.info("Connecting to %s" % sensor.name)
#				try:
#					s.connect()
#					self.sensors.append(s)
#				except Exception as e:
#					self.logger.error("Unable to connect to sensor %s: %s" % (s.sensor.name, str(e)))
#					s.disconnect()
	
	def probe(self):
		if (self.numberOfSamples == 0):
			self.logger.info("Starting sampling. Going to sample indefinitely at a rate of 1 every %d seconds." % self.sampleRate)
		else:
			self.logger.info("Starting sampling. Going to collect %d samples at a rate of 1 every %d seconds." % (self.numberOfSamples, self.sampleRate))
		i = 0
		while 1:
			start_time = time.time()
			self.logger.info("Gathering data sample %d" % i)
			i += 1
			for sensor in self.sensors:
				self.logger.info("Probing %s" % sensor.sensor.name)
				try:
					sensor.read()
				except Exception as e:
					self.logger.error("Exception (%s): %s" % (sensor.sensor.name, str(e)))
			elapsed_time = time.time() - start_time
			self.logger.info("Done.")
			if (i == self.numberOfSamples):
				break
			self.logger.info("Sleeping %d seconds until next sample" % self.sampleRate)
			time.sleep(self.sampleRate - elapsed_time)
	
		self.cleanup()
		
	def cleanup(self):
		self.logger.debug("Disconnecting from sensors")
		for sensor in self.sensors:
			sensor.disconnect()