from django.utils import timezone
from weatherapp.models import Sensor, DataType, WeatherData

class SensorBase(object):
	# Sensor Data types as known by the sensor library
	NUMBER_OF_DATATYPES = 9
	Temperature_F, Humidity_Percent, Dewpoint_F, BarometricPressure_inchesHg, RelativeLight_Percent, WindSpeed_mph, WindDirection_degrees, Rainfall_inches, BatteryLevel_volts = range(NUMBER_OF_DATATYPES)
	
	def __init__(self, sensor):
		self.sensor = sensor
		self.exceptions = 0;
	
	# Connect to the sensor device and prepare to read data
	# This function accepts an array of device-specific connection
	# parameters. Returns true on success or false on failure
	# OVERRIDE THIS FUNCTION IN YOUR SUBCLASS
	def connect(self):
		pass
	
	# Disconnect from the sensor device
	# OVERRIDE THIS FUNCTION IN YOUR SUBCLASS
	def disconnect(self):
		pass
	
	# Read one sample of data from sensor and save it to the database
	# OVERRIDE THIS FUNCTION IN YOUR SUBCLASS
	def read(self):
		pass
	
	# Call this function in your subclass after read() to save data to the database
	def _save(self, data):
		t = timezone.now()
		for key, value in data.items():
			datatype = DataType.objects.get(sensorlib_id = key)
			weather_datum = WeatherData(type = datatype, sensor = self.sensor, value = value, timestamp = t)
			weather_datum.save()