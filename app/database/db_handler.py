import uuid
from datetime import datetime, timedelta

from database.mongo_conn import *
from common.config import *
from common.utilities import *
from definitions.enums import *
from definitions.request_models import *


class TenantManagement():

	def __init__(self):
		self.db = TENANTS

	def create_tenant(self, tenant_info):
		if not self.get_tenant(tenant_info.username):
			tenant_info.creation_date=get_timestamp()
			return str(self.db.insert_one(tenant_info.dict()))
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
		return mongo2json(self.db.find_one(search), False)

	def find_many(self, search):
		return mongo2json(self.db.find_many(search, True))

	def update(self, search: dict, update: dict, upsert=True):
		return self.db.update_one(search, {"$set": update}, upsert=upsert)

	def store(self, model: dict):
		try:
			return str(self.db.insert_one(model))
		except Exception as e:
			logger.error(e)
