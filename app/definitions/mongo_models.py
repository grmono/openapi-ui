from common.config import *
from pydantic import BaseModel, create_model, ValidationError, validator, HttpUrl, EmailStr
from typing import List, Union, Dict, Optional
from email_validator import validate_email, EmailNotValidError
from definitions.enums import *


class BuildLogs(BaseModel):
    logs: str
    user: str
    file_size: int = 0
    datetime: str
    url: str = None
    language: str
    operation_id: str
    file_size: int = 0
    type: LogTypes = LogTypes.Build.value


class TaskStatus(BaseModel):
    uuid: str
    user: str = None
    group: str = None
    type: str = 'build_sdk'
    project: str = None
    status: TaskState = TaskState.PENDING.value
