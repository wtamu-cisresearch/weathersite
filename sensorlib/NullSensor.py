from SensorBase import SensorBase

class NullSensor(SensorBase):
	def __init__(self, sensor):
		super(NullSensor, self).__init__(sensor)
	
	def read(self):
		data = {self.Temperature_F: 0,
				self.Humidity_Percent: 0,
				self.Dewpoint_F: 0,
				self.BarometricPressure_inchesHg: 0,
				self.RelativeLight_Percent: 0,
				self.WindSpeed_mph: 0,
				self.WindDirection_degrees: 0,
				self.Rainfall_inches: 0,
				self.BatteryLevel_volts: 0}
		
		super(NullSensor, self)._save(data)