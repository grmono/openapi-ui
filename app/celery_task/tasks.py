import datetime
import json
import re
import os
import requests
import subprocess
import tempfile
import uuid
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


@celery_worker.task(name='build_sdk.task', bind=False)
def build_sdk_from_url(url: HttpUrl, language: SupportedLanguages, user: str, operation_id: str):
	search = {'uuid': operation_id}
	handler = GenericMongoHandler(TASKS)
	builds = GenericMongoHandler(BUILDS)
	try:
		handler.update(search, {'status': TaskState.RUNNING.value})
		temp_dir = tempfile.mkdtemp()
		language = str(language.lower())
		command = f"""java -jar {OPEN_API_GEN} -i {url} -g {language} -o {temp_dir}"""
		logs = check_output(command.split(" "))
		# logs = subprocess.call(command.split(" "))
		data = BuildLogs(
			user = user,
			logs = logs,
			url = url,
			datetime = get_timestamp(),
			language = language,
			operation_id = operation_id
		)
		builds.store(data.dict())
		temp_dir_size = get_size(temp_dir)
		if temp_dir_size:
			data.file_size = temp_dir_size
			os.system(f"tar -cvf {operation_id}.tar {temp_dir}")
			os.system(f"gzip {operation_id}.tar")
			read_file = Path(f"{operation_id}.tar")
			GenericGridFSHandler().store(bytes(read_file), operation_id)
			os.remove(f"{operation_id}.tar")
		os.rmdir(temp_dir)
		handler.update(search, {'status': TaskState.FINISHED.value})
		return data.dict()
	except Exception as e:
		logger.error(e)
		update = {'status': TaskState.FAILED.value, 'error': str(e)}
		handler.update(search, update)
