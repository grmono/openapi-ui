import json
from database.mongo_conn import *
from common.config import *
import uuid
from common.utilities import *
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from definitions.enums import *
from bson import json_util


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


class GenericGridFSHandler():

	def __init__(self):
		self.db = gridfs.GridFS(gridfsdb)

	def store(self, bin, uuid=None):
		if uuid:
			self.db.put(bin, uuid=uuid)
		else:
			self.db.put(bin)


class GenericMongoHandler():

	def __init__(self, database: str):
		self.db = database

	def find_one(self, search):
		return json_util.dumps(self.db.find_one(search))

	def find_many(self, search):
		return json_util.dumps(list(self.db.find_many(search)))

	def update(self, search: dict, update: dict, upsert=True):
		return self.db.update_one(search, {"$set": update}, upsert=upsert)

	def store(self, model: dict):
		try:
			return str(self.db.insert(model))
		except Exception as e:
			logger.error(e)
