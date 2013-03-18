import feedparser
from SensorBase import SensorBase

class YahooWeather(SensorBase):
	def __init__(self, sensor):
		super(YahooWeather, self).__init__(sensor)
	
	def read(self):
		d = feedparser.parse('http://weather.yahooapis.com/forecastrss?w=' + self.sensor.address + '&u=f')
		
		try:
			data = {self.Temperature_F: float(d.entries[0]['yweather_condition']['temp']),
					self.Humidity_Percent: float(d['feed']['yweather_atmosphere']['humidity']),
					self.BarometricPressure_inchesHg: float(d['feed']['yweather_atmosphere']['pressure']),
					self.WindSpeed_mph: float(d['feed']['yweather_wind']['speed']),
					self.WindDirection_degrees: float(d['feed']['yweather_wind']['direction'])}
			super(YahooWeather, self)._save(data)
		except:
			self.exceptions += 1
			raise Exception("Data sample contains invalid values for sensor " + self.sensor.name + ".")