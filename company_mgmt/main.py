from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from common import common
from services import company
from fastapi import Request
from fastapi.testclient import TestClient

app = FastAPI()
def test_client():
    return TestClient(app)

app.include_router(company.router)

LOGGER = common.LOGGER


@app.exception_handler(common.customException)
async def custom_exception_handler(request: Request, exc: common.customException):
    content = {"message": [exc.message]}
    if exc.alert_info:
        content["alert_info"] = exc.alert_info

    LOGGER.info({"status_code": exc.status_code})
    LOGGER.info({"content": content})
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    return response
