from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from api.v1.routers import routers
from core.config import settings
from core.http_connector import ExternalServiceConnector
from core.logger import LoggerConfig
from modules.services.users.user_serv import UserService
from modules.unit_of_works.users.user_uow import UserUOW


# # region ------------------------------ initialize ----------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:  # noqa
    ExternalServiceConnector.start_client()

    async with UserUOW() as uow:
        await UserService.create_doctor_user(uow, settings.auth.doctor_username, settings.auth.doctor_email,
                                             settings.auth.doctor_password)

    yield
    await ExternalServiceConnector.close_client()
# endregion -------------------------------------------------------------------------


# region ---------------------------- APPLICATION -----------------------------------
app = FastAPI(
    lifespan=lifespan,
    openapi_url=settings.openapi_url,
    swagger_ui_init_oauth={
        "clientId": settings.client_id,
        "clientSecret": settings.client_secret,
    },
)


# endregion -------------------------------------------------------------------------


# region -------------------------------- SWAGGER -----------------------------------
def custom_openapi():
    """Swagger configuration."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="TestProject",
        version="1.0",
        summary="Project related to testproject",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
# endregion -------------------------------------------------------------------------


# region -------------------------------- MIDDLEWARES --------------------------------------
# CORS configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# endregion -------------------------------------------------------------------------

# region -------------------------------- Routing -----------------------------------
for router in routers:
    app.include_router(router)
#endregion -------------------------------------------------------------------------
if __name__ == "__main__":
    # in production use gunicorn
    uvicorn.run(
        app="main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_config=LoggerConfig.execute_config(),
    )
