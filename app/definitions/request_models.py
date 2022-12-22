from common.config import *
from pydantic import BaseModel, create_model, ValidationError, validator, HttpUrl, EmailStr
from typing import List, Union, Dict, Optional
from email_validator import validate_email, EmailNotValidError
from definitions.enums import *
################################################################################
# NIC REQUEST MODELS
################################################################################
################################################################################
# MONGO
################################################################################

class CreateTenant(BaseModel):
	password: str
	username: str
	locked: bool = False
	email: EmailStr
	firstname: str = None
	lastname: str = None
	creation_date: str = None
	@validator("password")
	def crypt_pass(cls, v):
		return bcrypt.hashpw(v.encode(), salt)
