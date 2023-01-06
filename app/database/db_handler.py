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

	def remove_tenant(self, username):
		return self.db.remove({'username': username})

	def edit_tenant(self, username, info: dict):
		return self.db.update_one({'username': username}, {"$set": info}, upsert=False)


class GenericGridFSHandler():

	def __init__(self):
		self.db = gridfs.GridFS(gridfsdb)

	def store(self, bin, uuid=None):
		if uuid:
			self.db.put(bin, uuid=uuid)
		else:
			self.db.put(bin)


class GenericMongoHandler():

	def __init__(self, database):
		self.db = database

	def find_one(self, search):
		return mongo2json(self.db.find_one(search, {"_id": 0}), False)

	def find(self, search):
		return mongo2json(self.db.find(search), True)

	def update(self, search: dict, update: dict, upsert=True):
		return self.db.update_one(search, {"$set": update}, upsert=upsert)

	def store(self, model: dict):
		try:
			return str(self.db.insert_one(model))
		except Exception as e:
			logger.error(e)


class UserMongoHandler():


	def __init__(self, database, credentials):
		self.db = database
		self.username = credentials.username

	def find_one(self, search: dict):
		search['user'] = self.username
		return mongo2json(self.db.find_one(search, {"_id": 0}), False)

	def find(self, search: dict):
		search['user'] = self.username
		return mongo2json(self.db.find(search))

	def update(self, search: dict, update: dict, upsert=True):
		search['user'] = self.username
		return self.db.update_one(search, {"$set": update}, upsert=upsert)

	def store(self, model: dict):
		try:
			model['user'] = self.username
			return str(self.db.insert_one(model))
		except Exception as e:
			logger.error(e)

	def remove(self, model: dict):
		try:
			model['user'] = self.username
			self.db.remove(model)
			return True
		except Exception as e:
			logger.error(e)
