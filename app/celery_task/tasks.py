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
	user_handler = GenericMongoHandler(USER_SSH_KEYS)
	documents.store({
		'uuid': operation_id,
		'file': encoded,
		'datetime': get_timestamp(),
		'project': project_name
		}
	)
	handler.update(search, {'status': TaskState.FINISHED.value})
	settings = settings_search.find_one({'project': project_name})
	if settings.get("push_to_git"):
		ssh_key = user_handler.find_one({'user': settings.get('user')})
		if ssh_key:
			ssh_key = ssh_key.get('ssh_key')
		else:
			logger.warning('User does not have an ssh key')
		git_url = settings.get("push_to_git")
		## Implement git commit to repo

	return True


@celery_worker.task(name='build_sdk_url.task', bind=False)
def build_sdk_from_url(url: HttpUrl, language: SupportedLanguages, user: str, operation_id: str, project_name: str = None):
	search = {'uuid': operation_id}
	handler = GenericMongoHandler(TASKS)
	builds = GenericMongoHandler(BUILDS)

	try:
		headers = {'Content-Type':'application/json'}
		request_data = OpenAPIRequest(openAPIUrl=url).dict()
		language = str(language.lower())
		handler.update(search, {'status': TaskState.RUNNING.value})
		generator_url = f'http://{OPENAPI_GENERATOR}/api/gen/clients/{language}'
		logger.info(f"Sending Request to generator url:{generator_url}")
		response = requests.post(url=generator_url, json=request_data, headers=headers)
		logger.info("Received response")
		logger.info(response.text)
		data = BuildLogs(
			user = user,
			logs = response.text,
			project = project_name,
			url = url,
			datetime = get_timestamp(),
			language = language,
			operation_id = operation_id
		)
		builds.store(data.dict())
		if response.status_code != 200:
			raise Exception("Generator error")

		response = json.loads(response.text)
		link = response.get('link')
		response = requests.get(url=link, allow_redirects=True)
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
		headers = {'Content-Type':'application/json'}
		request_data = OpenAPIRequest(spec=url).dict()
		language = str(language.lower())
		handler.update(search, {'status': TaskState.RUNNING.value})
		response = requests.post(url=f'http://{OPENAPI_GENERATOR}/api/gen/clients/{language}', json=request_data, headers=headers)
		data = BuildLogs(
			user = user,
			project = project_name,
			logs = response.text,
			datetime = get_timestamp(),
			language = language,
			operation_id = operation_id
		)
		builds.store(data.dict())
		if response.status_code != 200:
			raise Exception("Generator error")

		response = json.loads(response.text)
		link = response.get('link')
		response = requests.get(url=link, allow_redirects=True)
		if response.status_code != 200:
			raise Exception("Failed to download generated file")
		store_sdk(search, response, operation_id, project_name)
		return data.dict()
	except Exception as e:
		logger.error(e)
		update = {'status': TaskState.FAILED.value, 'error': str(e)}
		handler.update(search, update)
		return OperationError(error=str(e)).dict()
