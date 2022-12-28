#!/usr/bin/python3
import time
import random
import uvicorn
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Depends, Request, APIRouter
from fastapi_utils.tasks import repeat_every

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from content_size_limit_asgi import ContentSizeLimitMiddleware

from definitions.request_models import *
from definitions.response_models import *
from routers import generate, management, user_profile, register
from common.config import *
from auth import *


app = FastAPI(
	title="OPENAPI-UI",
	description="OPENAPI UI",
	version="0.0.1",
)

app.add_middleware(ContentSizeLimitMiddleware, max_content_size=512)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
	start_time = time.time()
	response = await call_next(request)
	process_time = time.time() - start_time
	response.headers["X-Process-Time"] = str(process_time)
	return response


@app.get("/login")
def login(creds = Depends(get_current_username)):
	return OperationSuccess().dict()


app.include_router(generate.router,
	prefix="/api/v1/build",
	tags=['SDK Generate'],
    dependencies=[Depends(get_current_username)],
	responses={404: {"description": "Not found"}})


app.include_router(management.router,
	prefix="/api/v1/management",
	tags=['Management'],
    dependencies=[Depends(get_current_username), Depends(only_management)],
	responses={404: {"description": "Not found"}})


app.include_router(user_profile.router,
	prefix="/api/v1/profile",
	tags=['Profile Management'],
    dependencies=[Depends(get_current_username)],
	responses={404: {"description": "Not found"}})


app.include_router(register.router,
	prefix="/api/v1/register",
	tags=['Registration'],
    dependencies=[Depends(get_current_username)],
	responses={404: {"description": "Not found"}})
