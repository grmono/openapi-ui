from fastapi import APIRouter, Request, HTTPException, Header, Depends
from error_handler import *
from fastapi.security import HTTPBasic, HTTPBasicCredentials

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
