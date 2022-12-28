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

@router.get("/projects")
def get_projects(settings: bool = False, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		res = UserMongoHandler(PROJECT_SETTINGS, credentials).find({})
		if not res:
			return OperationError(error='not found')
		elif settings:
			return res

		names = []
		for entry in res:
			names.append(entry.get('project'))
		return names
	except Exception as e:
		logger.error(e)
		abort(500)


@router.get("/{project}/settings")
def project_settings(project: str, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		res = UserMongoHandler(PROJECT_SETTINGS, credentials).find_one({'project': project})
		if not res:
			return OperationError(error='not found')
		return res
	except Exception as e:
		logger.error(e)
		abort(500)


@router.post("/create/project/base")
def create_project(setting: ProjectSettings, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		manage = UserMongoHandler(PROJECT_SETTINGS, credentials)
		setting.user = credentials.username
		if manage.find_one({'project': setting.project}):
			return OperationError(error='Project already exists')
		manage.store(setting.dict())
		return OperationSuccess()
	except Exception as e:
		logger.error(e)
		abort(500)


@router.put("/edit/project/base")
def edit_project(setting: ProjectSettings, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		manage = UserMongoHandler(PROJECT_SETTINGS, credentials)
		setting.user = credentials.username
		if not manage.find_one({'project': setting.project}):
			return OperationError(error='not found')
		manage.update({'project': setting.project}, setting.dict())
		return OperationSuccess()
	except Exception as e:
		logger.error(e)
		abort(500)


@router.delete("/delete/project/base")
def delete_project(project: str, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		manage = UserMongoHandler(PROJECT_SETTINGS, credentials)
		if not manage.find_one({'project': project}):
			return OperationError(error='not found')
		manage.remove({'project': project})
		return OperationSuccess()
	except Exception as e:
		logger.error(e)
		abort(500)


@router.post("/add/ssh/key")
def add_key(ssh_key: str, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		UserMongoHandler(USER_SSH_KEYS, credentials).store({'ssh_key': ssh_key})
		return OperationSuccess()
	except Exception as e:
		logger.error(e)
		abort(500)


@router.delete("/delete/ssh/key")
def delete_key(ssh_key: str, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		UserMongoHandler(USER_SSH_KEYS, credentials).remove({'ssh_key': ssh_key})
		return OperationSuccess()
	except Exception as e:
		logger.error(e)
		abort(500)


@router.get("/ssh/key")
def get_keys(credentials: HTTPBasicCredentials = Depends(security)):
	try:
		res = UserMongoHandler(USER_SSH_KEYS, credentials).find({})
		if res:
			return res
		return OperationError(error='not found')
	except Exception as e:
		logger.error(e)
		abort(500)
