from fastapi import APIRouter
from starlette.responses import Response
from api.dependencies.dependencies import UserServiceDep, UserUOWDep
from modules.responses.users import user as responses
from modules.schemas.users.auth import TokenInfoSchema
from modules.schemas.users.user import (
    RegisterSchema
)

user = APIRouter(prefix="/api/v1/user", tags=["User"])



@user.post("/register",
           summary="Register a new user",
           responses=responses.REGISTRATION_RESPONSES)
async def create_user(
    uow: UserUOWDep,
    service: UserServiceDep,
    model: RegisterSchema,
    response: Response,
) -> TokenInfoSchema:
    """Controller for registering a new user"""
    user_data = await service.create(uow, model)

    return
