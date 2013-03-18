import os
os.environ['DJANGO_SETTINGS_MODULE']='weathersite.settings'

import signal
import sys
import argparse
import logging
from sensorlib.DataGatherer import DataGatherer

def signal_handler(signal, frame):
	logger.info("User interrupted. Cleaning up and exiting.")
	myDataGatherer.cleanup()
	sys.exit(0)

def positive_int(value):
	ivalue = int(value)
	if ivalue < 0:
		raise argparse.ArgumentTypeError("invalid positive_int value: '%s'" % value)
	return ivalue
	
parser = argparse.ArgumentParser(description='Process some integers', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-s', '--sample-rate', default=900, type=positive_int, help="Rate at which to sample data from the sensors in seconds. Choose between 120 seconds (2 min) and 86400 seconds (24 hours)")
parser.add_argument('-n', '--number', default=0, type=positive_int, help="Number of samples to take. 0 means keep sampling indefinitely")
parser.add_argument('-q', '--quiet', action='store_true', help="Log to the log file instead of the console")

args = parser.parse_args()
if (args.sample_rate < 120):
	args.sample_rate = 120
if (args.sample_rate > 86400):
	args.sample_rate = 86400

logger = logging.getLogger('weathersite.console')
if (args.quiet):
	logger = logging.getLogger('weathersite.weatherapp')

signal.signal(signal.SIGINT, signal_handler)
myDataGatherer = DataGatherer(args.sample_rate, args.number, logger)
myDataGatherer.probe()