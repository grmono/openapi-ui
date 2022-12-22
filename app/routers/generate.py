from fastapi import APIRouter, Request, HTTPException, Header, Depends
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


@router.post("")
def build_sdk(language: SupportedLanguages, url: HttpUrl, project_name: str = None, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		task = TaskStatus(uuid=str(uuid.uuid4()), user=credentials.username)
		GenericMongoHandler(TASKS).store(task.dict())
		build_sdk_from_url.apply_async(args=[url, language, credentials.username, task.uuid])
		return task.dict()
	except Exception as e:
		logger.error(e)
		abort(500)


@router.get("/task/status")
def build_status(uuid=None, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		if uuid:
			res = GenericMongoHandler(TASKS).find_one({'uuid': uuid, 'user': credentials.username})
			if res.get("status") in [TaskState.FINISHED.value, TaskState.FAILED.value]:
				GenericMongoHandler(BUILDS).find_one({'uuid': uuid, 'user': credentials.username})
		else:
			return GenericMongoHandler(TASKS).find_many({'user': credentials.username})
	except Exception as e:
		logger.error(e)
		abort(500)
