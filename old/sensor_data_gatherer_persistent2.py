from sensorlib.SensorBase import SensorBase
from sensorlib.NullSensor import NullSensor
from sensorlib.USBWeatherBoard import USBWeatherBoard
from sensorlib.YahooWeather import YahooWeather
from weatherapp.models import Sensor, DataType, WeatherData, SensorModel
import time

sensors = []
for sensor in Sensor.objects.all():
	s = 0
	if (sensor.model.name == "NullSensor"):
		s = NullSensor(sensor)
	elif (sensor.model.name == "USBWeatherBoard"):
		s = USBWeatherBoard(sensor)
	elif (sensor.model.name == "YahooWeather"):
		s = YahooWeather(sensor)
	
	if (s):
		print "Connecting to " + sensor.name
		try:
			s.connect()
			sensors.append(s)
		except Exception as e:
			print "Unable to connect to sensor", s.name, ": ", str(e)
			s.disconnect()

i = 1
while 1:
	start_time = time.time()
	print "\nGathering data sample ", i
	i = i + 1
	for sensor in sensors:
		print "Probing " + sensor.sensor.name
		try:
			sensor.read()
		except Exception as e:
			print "Exception (", sensor.sensor.name, "): ", str(e)
	elapsed_time = time.time() - start_time
	print "Done. Sleeping 15 minutes."
	time.sleep(900 - elapsed_time)

		
for sensor in sensors:
	sensor.disconnect()