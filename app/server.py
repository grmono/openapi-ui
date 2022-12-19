#!/usr/bin/python3
import time
import random

from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Depends, Request, APIRouter

from definitions.request_models import *
from definitions.response_models import *

from routers import generate

from common.config import *
from auth import *

from fastapi_utils.tasks import repeat_every


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
	start_time = time.time()
	response = await call_next(request)
	process_time = time.time() - start_time
	response.headers["X-Process-Time"] = str(process_time)
	return response


# @repeat_every(seconds=3600)
# def periodic_registration_search():
#     CYDomainHandler().retrieved_domain_registration()
#
# @repeat_every(seconds=3600)
# def periodic_charge_check():
#     CYDomainCharger().check_for_charge()


@app.get("/login")
def login(creds = Depends(get_current_username)):
	return OperationSuccess().dict()


app.include_router(search.router,
	prefix="/api/v1/search",
	tags=['Domain Search'],
    dependencies=[Depends(get_current_username)],
	responses={404: {"description": "Not found"}})