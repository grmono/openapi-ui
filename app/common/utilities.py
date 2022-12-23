#!/usr/bin/env python3
import os
import re
import requests
import json
import uuid
from bson.objectid import ObjectId
from bson import json_util
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


def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def mongo2json(object, many=True):
	if many:
		return json.loads(json_util.dumps(list(object)))
	return json.loads(json_util.dumps(object))
