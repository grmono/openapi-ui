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
		command = f"""java -jar {OPEN_API_GEN} -i {openapi_url} -g {language} -o {temp_dir}"""
		logs = subprocess.call(command.split(" "))
		data = ContainersLogs(
			user = user,
			logs = logs,
			datetime = get_timestamp(),
			language = language,
			operation_id = operation_id
		)
		builds.store(data)
		temp_dir_size = get_size(temp_dir)
		if temp_dir_size:
			data.file_size = temp_dir_size
			os.system(f"tar -cvf {uuid}.tar {temp_dir}")
			os.system(f"gzip {uuid}.tar")
			read_file = Path(f"{uuid}.tar")
			GenericGridFSHandler().store(bytes(read_file), operation_id)
			os.remove(f"{uuid}.tar")
		os.rmdir(temp_dir)
		handler.update(search, {'status': TaskState.FINISHED.value})
		return data.dict()
	except Exceptions as e:
		logger.error(e)
		update = {'status': TaskState.FAILED.value, 'error': str(e)}
		handler.update(search, update)
