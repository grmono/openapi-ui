#!/usr/bin/env python3
import os
import sys
import stripe
import bcrypt
import logging
import datetime
from logging.handlers import RotatingFileHandler
from logstash_formatter import LogstashFormatter
from dotted_dict import DottedDict
from fastapi import FastAPI

salt = bcrypt.gensalt()


##########################################################################
# APP CONFIG
##########################################################################
APP_HOST = "127.0.0.1"
APP_PORT = os.getenv("API_PORT", 8000)
APP_DEBUG = True
APP_RELOAD = True
LOGFILE = "/tmp/api.log"
LOG_LEVEL = 'debug'
API_ROOT_PATH = ""
################################################################################
# MONGO
################################################################################
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'admin'
MONGO_PASSWORD = ''
MONGO_DB = 'api'
GRIDFS_DB = 'gridfs'
##########################################################################
# RestAPI CONFIG
##########################################################################
app = FastAPI(
	title="OPENAPI-UI",
	description="OPENAPI UI",
	version="0.0.1",
)
REGISTER_USER_ALLOWED_ROLE = ['admin', 'frontend']
BLOCK_REGISTRATION = False

##########################################################################
# LOGGING CONFIG
##########################################################################
root = logging.getLogger('uvicorn')

if len(root.handlers) == 0:
    hdlr = RotatingFileHandler(LOGFILE, maxBytes=1024*1024*500, backupCount=4)
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = LogstashFormatter()
    hdlr.setFormatter(formatter)
    root.addHandler(hdlr)

logger = root
