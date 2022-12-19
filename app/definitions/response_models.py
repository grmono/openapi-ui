from pydantic import BaseModel
from pydantic import BaseModel, create_model
from typing import List, Union
from definitions.enums import *


class OperationError(BaseModel):
	error: str
	operation: bool = False


class OperationSuccess(BaseModel):
	operation: bool = True
