from fastapi import APIRouter, Request, HTTPException, Header, Depends, File, UploadFile
from error_handler import *
from fastapi.security import HTTPBasic, HTTPBasicCredentials



from definitions.response_models import *
from definitions.request_models import *
from definitions.enums import *

from common.config import *
from common.utilities import *

from database.db_handler import *
from celery_task.tasks import *

import uuid

security = HTTPBasic()
router = APIRouter()


@router.post("/url")
def build_sdk_url(language: SupportedLanguages, url: HttpUrl, project_name: str = None, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		task = TaskStatus(uuid=str(uuid.uuid4()), user=credentials.username)
		GenericMongoHandler(TASKS).store(task.dict())
		build_sdk_from_url.apply_async(args=[url, language, credentials.username, task.uuid])
		return task.dict()
	except Exception as e:
		logger.error(e)
		abort(500)


@router.post("/file")
def build_sdk_file(language: SupportedLanguages, file: UploadFile = File(...), project_name: str = None, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		task = TaskStatus(uuid=str(uuid.uuid4()), user=credentials.username)
		GenericMongoHandler(TASKS).store(task.dict())
		build_sdk_from_url.apply_async(args=[file, language, credentials.username, task.uuid])
		return task.dict()
	except Exception as e:
		logger.error(e)
		abort(500)


@router.get("/task/status")
def build_status(uuid: str = None, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		if not uuid:
			logger.info("Checking for users total tasks")
			return GenericMongoHandler(TASKS).find_many({'user': credentials.username})
		else:
			res = GenericMongoHandler(TASKS).find_one({'uuid': uuid, 'user': credentials.username})

		if not res:
			logger.info("nothing found")
			return OperationError(error='uuid doesnt exist').dict()
		elif res.get("status") in [TaskState.FINISHED.value, TaskState.FAILED.value]:
			logger.info("Checking for completed tasks")
			build_res = GenericMongoHandler(BUILDS).find_one({'operation_id': uuid, 'user': credentials.username})
			res['build'] = build_res
			return res
		else:
			return res
	except Exception as e:
		logger.error(e)
		abort(500)
