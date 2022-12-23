from error_handler import abort
from common.config import *
from common.utilities import *
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from definitions.request_models import CreateTenant
from database.db_handler import *

security = HTTPBasic()


if ADMIN_USER and ADMIN_PASS:
	TenantManagement().create_tenant(CreateTenant(
		username=ADMIN_USER,
		password=ADMIN_PASS,
		email='administrator@system.com'))


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
	try:
		tenant_info = TenantManagement().get_tenant(credentials.username)
		logger.info(tenant_info)
		if not tenant_info or not bcrypt.checkpw(credentials.password.encode(), tenant_info.get('password')):
			logger.info(f"Tenant:{tenant_info} failed to authenticated")
			abort(401)
		elif tenant_info.get('locked'):
			logger.warning(f"Blocked Tenant:{tenant_info} attempted to authenticate")
			abort(403)
		else:
			logger.warning(f"Tenant validated succesfully")
		return credentials
	except Exception as e:
		logger.error(e)
		abort(401)
