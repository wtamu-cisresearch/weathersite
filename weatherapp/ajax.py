from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
import logging
logger = logging.getLogger('weathersite.weatherapp')

@dajaxice_register
def sayhello(request):
	logger.debug("ajax test")
	return simplejson.dumps({'message':'Hello World'})