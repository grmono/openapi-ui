#!/usr/bin/env python3
import os
import sys
import bcrypt
import logging
import datetime
from logging.handlers import RotatingFileHandler
from logstash_formatter import LogstashFormatter
from dotted_dict import DottedDict

salt = bcrypt.gensalt()


##########################################################################
# APP CONFIG
##########################################################################
APP_HOST = "0.0.0.0"
APP_PORT = os.getenv("API_PORT", 8000)
APP_DEBUG = True
APP_RELOAD = True
LOGFILE = "/tmp/api.log"
LOG_LEVEL = 'debug'
API_ROOT_PATH = ""
REDIS_INSTANCE = os.getenv("REDIS_URI", "redis://:@localhost:6379")
OPENAPI_GENERATOR = os.getenv("OPENAPI_GENERATOR", "10.0.0.10:8081")

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")
################################################################################
# MONGO
################################################################################
MONGO_HOST =  os.getenv("MONGO_IP", "localhost")
MONGO_PORT = 27017
MONGO_USERNAME = 'admin'
MONGO_PASSWORD = ''
MONGO_DB = 'api'
GRIDFS_DB = 'gridfs'
##########################################################################
# RestAPI CONFIG
##########################################################################
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
