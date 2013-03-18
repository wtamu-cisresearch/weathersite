import serial
#import socket
from SensorBase import SensorBase

class USBWeatherBoard(SensorBase):
	Serial, Network = range(2)
	def __init__(self, sensor):
		self.connected = False
		super(USBWeatherBoard, self).__init__(sensor)
	
	def __connectSerial(self):
		# Can throw SerialError or ValueError
		# FIXME: We need a timeout. What is the best way?
		self.connection = serial.Serial(self.sensor.address, 9600, timeout=120)
		
		# Each time you connect to the USBWeatherBoard, it has two initialization lines:
		# '\r\n'
		# 'RESET\r\n'
		self.connection.readline()
		self.connection.readline()
		self.connectionType = self.Serial
		self.connected = True
		
	def __connectNetwork(self):
		# FIXME: Figure out port
		# FIXME: self.connection.settimeout() to something reasonable
		raise NotImplementedError("USBWeatherBoard: Network connections not implemented.")
		#self.connection = socket.socket()
		#self.connection.connect((self.sensor.address, port))
		#self.connectionType = Network
		#self.connected = True
		
	def connect(self):
		if (self.connected):
			return
	
		try:
			self.__connectNetwork()
			return
		except:
			try:
				self.__connectSerial()
				return
			except:
				pass
		self.exceptions += 1
		raise Exception("Unable to connect to sensor " + self.sensor.name + ".")
			
	def disconnect(self):
		if (self.connected):
			self.connection.close()
			self.connected = False
			
	def read(self):
		if (not self.connected):
			self.connect()
		
		if (self.connectionType == self.Serial):
			rawData = self.connection.readline()
		elif (self.connectionType == self.Network):
			# FIXME: Write this code
			return
		
		dataArray = rawData.split(',')
		if (len(dataArray) != 11 or dataArray[0] != '$' or dataArray[10][0] != '*'):
			self.exceptions += 1
			raise Exception("Corrupt data sample for sensor " + self.sensor.name + ": '" + rawData + "'")

		try:
			data = {self.Temperature_F: float(dataArray[1]),
					self.Humidity_Percent: float(dataArray[2]),
					self.Dewpoint_F: float(dataArray[3]),
					self.BarometricPressure_inchesHg: float(dataArray[4]),
					self.RelativeLight_Percent: float(dataArray[5]),
					self.WindSpeed_mph: float(dataArray[6]),
					self.WindDirection_degrees: float(dataArray[7]),
					self.Rainfall_inches: float(dataArray[8]),
					self.BatteryLevel_volts: float(dataArray[9])}
			super(USBWeatherBoard, self)._save(data)
		except:
			self.exceptions += 1
			raise Exception("Data sample contains invalid values for sensor " + self.sensor.name + ".")