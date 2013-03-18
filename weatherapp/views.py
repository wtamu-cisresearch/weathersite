# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from weatherapp.models import Sensor, DataType, WeatherData
from django.utils import simplejson, timezone
from django.conf import settings
import time
import logging
logger = logging.getLogger('weathersite.weatherapp')

def index(request):
	logger.debug("index requested.")
	sensor_list = Sensor.objects.all()
	datatype_list = DataType.objects.all()
	return render_to_response('weatherapp/index.html', {'sensor_list': sensor_list, "datatype_list": datatype_list}, context_instance=RequestContext(request))

def data_handler(request):
	logger.debug("data_handler called.")
	sensor_id = request.POST['sensor_id']
	datatype_id = request.POST['datatype_id']
	weather_data = WeatherData.objects.filter(sensor__id=sensor_id, type__id=datatype_id)
	datatype = DataType.objects.get(pk=datatype_id)
	data_points = []
	for d in weather_data:
		localtime = timezone.localtime(d.timestamp)
		# flot treats all timestamps as if they were UTC. We have to add our
		# local timezone offset to make them display correct
		flot_utcfix = localtime + localtime.utcoffset()
		js_timestamp = int(time.mktime(flot_utcfix.timetuple())) * 1000
		data_points.append([js_timestamp, d.value])

	return HttpResponse(simplejson.dumps({'data':data_points, 'units':datatype.units}))