import datetime
import json
import re
import os
import requests
import subprocess
import tempfile
import uuid
import bson
import base64
import shutil

from bson.binary import Binary
from pathlib import Path
from dotted_dict import DottedDict
from subprocess import check_output

from common.utilities import *
from common.config import *

from database.db_handler import *

from definitions.response_models import *
from definitions.enums import *
from definitions.request_models import *
from definitions.mongo_models import *

from celery_task.worker import celery_worker

def store_sdk(search, encoded, operation_id, project_name):
	documents = GenericMongoHandler(DOCUMENTS)
	handler = GenericMongoHandler(TASKS)
	settings_search = GenericMongoHandler(PROJECT_SETTINGS)
	tenant_manage = TenantManagement()
	documents.store({
		'uuid': operation_id,
		'file': encoded,
		'datetime': get_timestamp(),
		'url': url,
		'project': project_name
		}
	)
	handler.update(search, {'status': TaskState.FINISHED.value})
	settings = settings_search.find_one({'project': project_name})
	if settings.get("push_to_git"):
		user_info = tenant_manage.find(settings.user)
		ssh_key = user_info.get('ssh_key')
		git_url = settings.get("push_to_git")
		## Implement git commit to repo

	return True


@celery_worker.task(name='build_sdk_url.task', bind=False)
def build_sdk_from_url(url: HttpUrl, language: SupportedLanguages, user: str, operation_id: str, project_name: str = None):
	search = {'uuid': operation_id}
	handler = GenericMongoHandler(TASKS)
	builds = GenericMongoHandler(BUILDS)

	try:
		request_data = OpenAPIRequest(openAPIUrl=url).dict()
		language = str(language.lower())
		handler.update(search, {'status': TaskState.RUNNING.value})
		response = request.post(url=f'http://{OPENAPI_GENERATOR}/api/gen/clients/{language}', data=request_data)
		data = BuildLogs(
			user = user,
			logs = response,
			url = url,
			datetime = get_timestamp(),
			language = language,
			operation_id = operation_id
		)
		builds.store(data.dict())
		if response.status_code != 200:
			raise Exception("Generator error")

		link = response.get('link')
		response = request.get(url=link, allow_redirects=True)
		if response.status_code != 200:
			raise Exception("Failed to download generated file")
		store_sdk(search, response, operation_id, project_name)
		return data.dict()
	except Exception as e:
		logger.error(e)
		update = {'status': TaskState.FAILED.value, 'error': str(e)}
		handler.update(search, update)
		return OperationError(error=str(e)).dict()


@celery_worker.task(name='build_sdk_url.task', bind=False)
def build_sdk_from_spec(spec: dict, language: SupportedLanguages, user: str, operation_id: str, project_name: str = None):
	search = {'uuid': operation_id}
	handler = GenericMongoHandler(TASKS)
	builds = GenericMongoHandler(BUILDS)
	documents = GenericMongoHandler(DOCUMENTS)

	try:
		request_data = OpenAPIRequest(spec=url).dict()
		language = str(language.lower())
		handler.update(search, {'status': TaskState.RUNNING.value})
		response = request.post(url=f'http://{OPENAPI_GENERATOR}/api/gen/clients/{language}', data=request_data)
		data = BuildLogs(
			user = user,
			logs = response,
			datetime = get_timestamp(),
			language = language,
			operation_id = operation_id
		)
		builds.store(data.dict())
		if response.status_code != 200:
			raise Exception("Generator error")

		link = response.get('link')
		response = request.get(url=link, allow_redirects=True)
		if response.status_code != 200:
			raise Exception("Failed to download generated file")
		store_sdk(search, response, operation_id, project_name)
		return data.dict()
	except Exception as e:
		logger.error(e)
		update = {'status': TaskState.FAILED.value, 'error': str(e)}
		handler.update(search, update)
		return OperationError(error=str(e)).dict()
