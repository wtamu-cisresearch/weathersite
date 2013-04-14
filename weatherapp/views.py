# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from weatherapp.models import Sensor, DataType, WeatherData
from django.utils import simplejson, timezone
from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
from django.core.servers.basehttp import FileWrapper
import csv
import time
import logging
import os
logger = logging.getLogger('weathersite.weatherapp')

def index(request):
	logger.debug("index requested.")
	sensor_list = Sensor.objects.all()
	datatype_list = DataType.objects.all()
	return render_to_response('weatherapp/index.html', {'sensor_list': sensor_list, "datatype_list": datatype_list}, context_instance=RequestContext(request))

def data_handler(request):
	sensor_ids = request.POST.getlist('sensor_ids[]')
	datatype_id = request.POST['datatype_id']
	logger.debug("Getting %s data for sensors %s.", datatype_id, sensor_ids)

	result = []
	for sensor_id in sensor_ids:
		sensor_id = int(sensor_id)
		sensor = Sensor.objects.get(pk=sensor_id)
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

		result.append({'data':data_points, 'label':sensor.name, 'points': {'show': True}, 'lines': {'show': True}, 'hoverable': True, 'clickable': True})
		
	return HttpResponse(simplejson.dumps(result))
	#return HttpResponse(simplejson.dumps({'data':data_points, 'units':datatype.units}))

def csv_export(request):
	logger.debug("csv export requested.")
	tmpfile = NamedTemporaryFile(suffix='.csv')
	csvwriter = csv.writer(tmpfile)
	# write csv headers
	csvwriter.writerow(['sensor_id', 'sensor_name', 'timestamp', 'value', 'value_name', 'value_units'])
	weather_data = WeatherData.objects.all()
	for d in weather_data:
		csvwriter.writerow([d.sensor.id, d.sensor.name, d.timestamp, d.value, d.type.name, d.type.units])
	wrapper = FileWrapper(tmpfile)
	logger.debug("Serving CSV file name=%s length=%s", tmpfile.name, tmpfile.tell())
	response = HttpResponse(wrapper, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=weather.csv'
	response['Content-Length'] = tmpfile.tell()
	tmpfile.seek(0)
	return response