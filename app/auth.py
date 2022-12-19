from error_handler import abort
from common.config import *
from common.utilities import *
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from definitions.request_models import CreateTenant
from database.db_handler import *

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    try:
        tenant_info = TenantManagement().get_tenant(credentials.username)
        logger.debug(credentials)
        if not tenant_info or not bcrypt.checkpw(credentials.password.encode(), tenant_info.get('password')):
            abort(401)
        elif tenant_info.get('locked'):
            abort(403)
        return credentials
    except Exception as e:
        logger.error(e)
        abort(401)
