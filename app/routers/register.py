from fastapi import APIRouter, Request, HTTPException, Header, Depends
from error_handler import *
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from database.db_handler import *

from definitions.response_models import *
from definitions.request_models import *
from definitions.mongo_models import *
from definitions.enums import *

from common.config import *
from common.utilities import *


security = HTTPBasic()
router = APIRouter()

# @router.get("/")
# def new_user_register(user_info: CreateTenant):
# 	try:
# 		res = UserMongoHandler(PROJECT_SETTINGS, credentials).find({})
#
# 		if not res:
# 			return OperationError(error='not found')
# 	except Exception as e:
# 		logger.error(e)
# 		abort(500)
