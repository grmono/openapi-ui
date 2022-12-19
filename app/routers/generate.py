from fastapi import APIRouter, Request, HTTPException, Header, Depends
from common.config import *
from common.utilities import *
from error_handler import *
from modules.cy_domains import *
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from definitions.response_models import *
from definitions.request_models import *
from database.db_handler import DomainUserSearcher


security = HTTPBasic()
router = APIRouter()


@router.get("/report")
def search_for_user_purchases(credentials: HTTPBasicCredentials = Depends(security)):
	try:
		handler = DomainUserSearcher()
		domains = handler.search_for_user_purchases(credentials.username)
		response = []
		for entry in domains:
			response.append(PurchaseReport(**entry).dict())
		return response
	except Exception as e:
		logger.error(e)
		abort(500)

@router.post("/account/information")
def store_account_info(data: AccountInformation, credentials: HTTPBasicCredentials = Depends(security)):
	try:
		data = AccountInformation(username = credentials.username)

		handler = DomainUserSearcher()
		domains = handler.search_for_user_purchases(credentials.username)
		response = []
		for entry in domains:
			response.append(PurchaseReport(**entry).dict())
		return response
	except Exception as e:
		logger.error(e)
		abort(500)
