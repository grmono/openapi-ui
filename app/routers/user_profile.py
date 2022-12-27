from fastapi import APIRouter, Request, HTTPException, Header, Depends
from error_handler import *
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from definitions.response_models import *
from definitions.request_models import *
from definitions.mongo_models import *
from definitions.enums import *

from common.config import *
from common.utilities import *


security = HTTPBasic()
router = APIRouter()


@router.get("/read/project/base")
def read_project(project: str, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		res = UserMongoHandler(PROJECT_SETTINGS, credentials.username).find_one({'project': setting.project})
		if not res:
			return OperationError(error='not found')
		return res
	except Exception as e:
		logger.error(e)
		abort(500)


@router.post("/create/project/base")
def create_project(setting: ProjectSettings, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		manage = UserMongoHandler(PROJECT_SETTINGS, credentials.username)
		setting.user = credentials.username
		if manage.find_one({'project': setting.project}):
			return OperationError(error='Project already exists')
		manage.store(setting.dict())
		return OperationSuccess()
	except Exception as e:
		logger.error(e)
		abort(500)


@router.post("/edit/project/base")
def edit_project(setting: ProjectSettings, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		manage = UserMongoHandler(PROJECT_SETTINGS, credentials.username)
		setting.user = credentials.username
		if not manage.find_one({'project': setting.project}):
			return OperationError(error='not found')
		manage.update({'project': setting.project}, setting.dict())
		return OperationSuccess()
	except Exception as e:
		logger.error(e)
		abort(500)
