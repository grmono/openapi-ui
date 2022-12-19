#!/usr/bin/env python3
import os
import re
import requests
from datetime import datetime as datetime
from pydantic import HttpUrl

from definitions.response_models import *



def get_timestamp():
	'''
		Generates and returns a timestamp
			Returns:
				: Timestamp (string)
	'''
	return str(datetime.utcnow().isoformat())


def get_future_timestamp(duration):
	return str(datetime.utcnow().isoformat() + datetime.timedelta(years=duration))


def enum_to_list(class_object):
	return list(map(lambda c: c.value, class_object))
