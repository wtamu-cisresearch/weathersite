class SensorError(Exception):
	errorStrings = {  1: "No connection address specified.",
					  2: "Corrupt data sample:",
					  3: "Unable to connect to sensor.",
					255: "Unspecified error."}
	def __init__(self, strerror = "Unspecified Error", errno = 255):
		self.errno = errno
		self.strerror = strerror

	def __str__(self):
		return repr(self.strerror)