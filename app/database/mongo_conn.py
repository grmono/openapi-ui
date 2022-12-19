import pymongo
from pymongo import MongoClient
import gridfs

from common.config import MONGO_HOST, MONGO_PORT, MONGO_DB


client = MongoClient(MONGO_HOST, int(MONGO_PORT), connect=False)

db = client[MONGO_DB]
gridfsdb = client[GRIDFS_DB]

TENANTS = db['tenants']
