from fastapi import APIRouter, Request, HTTPException, Header, Depends, File, UploadFile
from error_handler import *
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import FileResponse
import io
import base64
from starlette.responses import StreamingResponse

from definitions.response_models import *
from definitions.request_models import *
from definitions.enums import *

from common.config import *
from common.utilities import *

from database.db_handler import *
from celery_task.generate_tasks import *

import uuid

security = HTTPBasic()
router = APIRouter()


@router.post("/{project}/stub")
def build_stub(
	language: SupportedFrameworks,
	project: str,
	credentials: HTTPBasicCredentials = Depends(security)):
	try:
		settings = UserMongoHandler(PROJECT_SETTINGS, credentials).find_one({'project': project})
		if not settings:
			return OperationError(error='unknown project')

		task = TaskStatus(uuid=str(uuid.uuid4()), user=credentials.username, project=project)
		if settings.get('url'):
			GenericMongoHandler(TASKS).store(task.dict())
			build_stub_from_url.apply_async(args=[settings.get('url'), language, credentials.username, task.uuid, project])
		elif settings.get('api_spec'):
			GenericMongoHandler(TASKS).store(task.dict())
			build_stub_from_spec.apply_async(args=[settings.get('api_spec'), language, credentials.username, task.uuid, project])
		else:
			return OperationError(error="Must specify specification via URL or Spec File")
		return task.dict()
	except Exception as e:
		logger.error(e)
		abort(500)


@router.post("/{project}/sdk")
def build_sdk(
	language: SupportedLanguages,
	project: str,
	credentials: HTTPBasicCredentials = Depends(security)):
	try:
		settings = UserMongoHandler(PROJECT_SETTINGS, credentials).find_one({'project': project})
		if not settings:
			return OperationError(error='unknown project')

		task = TaskStatus(uuid=str(uuid.uuid4()), user=credentials.username, project=project)
		if settings.get('url'):
			GenericMongoHandler(TASKS).store(task.dict())
			build_sdk_from_url.apply_async(args=[settings.get('url'), language, credentials.username, task.uuid, project])
		elif settings.get('api_spec'):
			GenericMongoHandler(TASKS).store(task.dict())
			build_sdk_from_spec.apply_async(args=[settings.get('api_spec'), language, credentials.username, task.uuid, project])
		else:
			return OperationError(error="Must specify specification via URL or Spec File")
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
			build_res = GenericMongoHandler(BUILDS).find_one({'uuid': uuid, 'user': credentials.username})
			res['build'] = build_res
			return res
		else:
			return res
	except Exception as e:
		logger.error(e)
		abort(500)


@router.get("/download")
def download(uuid: str, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		if not GenericMongoHandler(TASKS).find_one({'uuid': uuid, 'user': credentials.username}):
			return OperationError(error='unknown uuid')

		res = GenericMongoHandler(DOCUMENTS).find_one({'uuid': uuid, 'user': credentials.username})
		if not res:
			return OperationError(error='not found')
		data = res['file']['$binary']['base64']
		data = data.encode('ascii')
		data = base64.b64decode(data)
		return StreamingResponse(io.BytesIO(data),
			media_type="application/zip",
			headers={'Content-Disposition':
				'attachment; filename="sdk.zip"'
			}
		)
	except Exception as e:
		logger.error(e)
		abort(500)
