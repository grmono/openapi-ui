import os
import tempfile #1

from common.config import *
from pydantic import BaseModel, create_model, ValidationError, validator, HttpUrl, EmailStr
from typing import List, Union, Dict, Optional
from email_validator import validate_email, EmailNotValidError
from definitions.enums import *
from openapi_spec_validator import validate_spec_url


class SSHKey(BaseModel):
	user: str
	ssh_key: str


class BuildLogs(BaseModel):
	logs: str
	user: str
	datetime: str
	url: str = ""
	language: str
	operation_id: str
	type: LogTypes = LogTypes.SDK.value
	project: str


class TaskStatus(BaseModel):
	uuid: str
	user: str = ""
	group: str = ""
	type: str = 'build_sdk'
	project: str
	status: TaskState = TaskState.PENDING.value


class ProjectSettings(BaseModel):
	project: str
	user: str
	group: str = ""
	url: HttpUrl = ""
	api_spec: dict = {}
	push_to_git: HttpUrl = ""
	description: str = ""

	@validator("url")
	def validate_url(cls, v):
		if v:
			try:
				validate_spec_url(v)
				return v
			except Exception as e:
				raise ValueError(str(e))

	@validator("api_spec")
	def validate_spec(cls, v):
		if v:
			try:
				validate_spec(v)
				return v
			except Exception as e:
				raise ValueError(str(e))
