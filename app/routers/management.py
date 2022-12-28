from fastapi import APIRouter, Request, HTTPException, Header, Depends
from error_handler import *
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from database.db_handler import *

from definitions.response_models import *
from definitions.request_models import *
from definitions.enums import *

from common.config import *
from common.utilities import *


security = HTTPBasic()
router = APIRouter()


@router.post("/create/user")
def create_user(tenant_info: CreateTenant, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		if TenantManagement().create_tenant(tenant_info):
			return OperationSuccess()
		else:
			return OperationError(error='Failed to create user')
	except Exception as e:
		logger.error(e)
		abort(500)


@router.put("/edit/user/{user}")
def edit_user(user: str, tenant_info: EditTenant, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		if TenantManagement().edit_tenant(user, tenant_info.dict(exclude_none=True)):
			return OperationSuccess()
		else:
			return OperationError(error='Failed to edit user')
	except Exception as e:
		logger.error(e)
		abort(500)


@router.delete("/remove/user/{user}")
def disable_user(user: str, wipe: bool = False, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		if wipe:
			TenantManagement().remove(user)
		else:
			TenantManagement().edit_tenant(user, EditTenant(locked=True).dict(exclude_none=True))
		return OperationSuccess()
	except Exception as e:
		logger.error(e)
		abort(500)
