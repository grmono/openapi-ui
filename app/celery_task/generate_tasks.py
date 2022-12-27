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


@celery_worker.task(name='build_stub_from_url.task', bind=False)
def build_stub_from_url(url: HttpUrl, language: SupportedLanguages, user: str, operation_id: str, project_name: str = None):
	return build_stub(language, user, operation_id, project_name, url)


@celery_worker.task(name='build_stub_from_spec.task', bind=False)
def build_stub_from_spec(spec: dict, language: SupportedLanguages, user: str, operation_id: str, project_name: str = None):
	return build_stub(language, user, operation_id, project_name, None, spec)



@celery_worker.task(name='build_sdk_from_url.task', bind=False)
def build_sdk_from_url(url: HttpUrl, language: SupportedLanguages, user: str, operation_id: str, project_name: str = None):
	return build_sdk(language, user, operation_id, project_name, url)


@celery_worker.task(name='build_sdk_from_spec.task', bind=False)
def build_sdk_from_spec(spec: dict, language: SupportedLanguages, user: str, operation_id: str, project_name: str = None):
	return build_sdk(language, user, operation_id, project_name, None, spec)


def push_to_git(project_name):
	settings_search = GenericMongoHandler(PROJECT_SETTINGS)
	settings = settings_search.find_one({'project': project_name})
	if settings.get("push_to_git"):
		ssh_key = user_handler.find_one({'user': settings.get('user')})
		if ssh_key:
			ssh_key = ssh_key.get('ssh_key')
		else:
			logger.warning('User does not have an ssh key')
		git_url = settings.get("push_to_git")
		## Implement git commit to repo


def store_generated_zip(search, encoded, operation_id, project_name, type=LogTypes.SDK.value):
	documents = GenericMongoHandler(DOCUMENTS)
	handler = GenericMongoHandler(TASKS)
	user_handler = GenericMongoHandler(USER_SSH_KEYS)
	documents.store({
		'uuid': operation_id,
		'file': encoded,
		'type': type,
		'datetime': get_timestamp(),
		'project': project_name
		}
	)
	handler.update(search, {'status': TaskState.FINISHED.value})
	return push_to_git(project_name)


def build_sdk(language, user, operation_id, project_name = None, url = None, spec = None):
	search = {'uuid': operation_id}
	handler = GenericMongoHandler(TASKS)
	builds = GenericMongoHandler(BUILDS)

	try:
		headers = {'Content-Type':'application/json'}
		if url:
			request_data = OpenAPIRequest(openAPIUrl=url).dict()
		else:
			request_data = OpenAPIRequest(spec=spec).dict()

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
		store_generated_zip(search, response, operation_id, project_name)
		return data.dict()
	except Exception as e:
		logger.error(e)
		update = {'status': TaskState.FAILED.value, 'error': str(e)}
		handler.update(search, update)
		return OperationError(error=str(e)).dict()


def build_stub(language, user, operation_id, project_name = None, url = None, spec = None):
	search = {'uuid': operation_id}
	handler = GenericMongoHandler(TASKS)
	builds = GenericMongoHandler(BUILDS)
	try:
		headers = {'Content-Type':'application/json'}
		if url:
			request_data = OpenAPIRequest(openAPIUrl=url).dict()
		else:
			request_data = OpenAPIRequest(spec=spec).dict()

		language = str(language.lower())
		handler.update(search, {'status': TaskState.RUNNING.value})
		generator_url = f'http://{OPENAPI_GENERATOR}/api/gen/servers/{language}'
		logger.info(f"Sending Request to generator url:{generator_url}")
		response = requests.post(url=generator_url, json=request_data, headers=headers)
		logger.info("Received response")
		logger.info(response.text)
		data = BuildLogs(
			user = user,
			logs = response.text,
			project = project_name,
			url = url,
			type = LogTypes.STUB.value,
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
		store_generated_zip(search, response, operation_id, project_name, LogTypes.STUB.value)
		return data.dict()
	except Exception as e:
		logger.error(e)
		update = {'status': TaskState.FAILED.value, 'error': str(e)}
		handler.update(search, update)
		return OperationError(error=str(e)).dict()
