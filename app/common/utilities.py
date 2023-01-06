#!/usr/bin/env python3
import os
import re
import requests
import base64,struct,sys,binascii
import json
import uuid
from bson.objectid import ObjectId
from bson import json_util
from datetime import datetime as datetime
from pydantic import HttpUrl

from definitions.response_models import *

from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename


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


def validate_ssh_key(key):
	array=key.split();
	# Each rsa-ssh key has 3 different strings in it, first one being
	# typeofkey second one being keystring third one being username .
	if len(array) != 3:
		return False
	typeofkey=array[0]
	string=array[1]
	username=array[2]
	# must have only valid rsa-ssh key characters ie binascii characters
	try:
		data=base64.decodestring(string)
		str_len = struct.unpack('>I', data[:4])[0]
	except Exception as e:
		return False

	# data[4:11] must have string which matches with the typeofkey , another ssh key property.
	if data[4:4+str_len] == typeofkey and int(str_len) == int(7):
		return True
	else:
		return False
