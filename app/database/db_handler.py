import json
from database.mongo_conn import *
from common.config import *
import uuid
from common.utilities import *
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from definitions.enums import *


class TenantManagement():

	def __init__(self):
		self.db = TENANTS

	def create_tenant(self, tenant_info):
		if not self.get_tenant(tenant_info.username):
			tenant_info.creation_date=get_timestamp()
			return self.db.insert_one(tenant_info.dict())
		else:
			logger.info("Cannot create account username already exists")

	def get_tenant(self, username):
		return self.db.find_one({'username': username})


class GridFSHandler():

	def __init__(self):
		self.db = gridfs.GridFS(gridfsdb)
